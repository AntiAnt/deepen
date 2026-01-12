import argparse
import json
import os
from typing import Dict
from urllib.parse import parse_qs, parse_qsl, urlparse

from reliquery import Relic

from pipeline.pipeline import get_pipeline_service

# yt_url = "https://www.youtube.com/watch?v=GFyijjy1KdU"
yt_url = "https://www.youtube.com/watch?v=YRMVTmbe-Is"


def get_pipeline_config(path: str) -> Dict:
    assert os.path.exists(path)
    config = None
    with open(path, "r") as f:
        config = json.loads(f.read())
    assert config is not None
    return config


def get_video_id_from_url(url: str) -> str:
    return parse_qs(urlparse(url).query).get("v", [None])[0]


def main():
    parser = argparse.ArgumentParser(
        description="Deepen pipeline: ingest, transcribe, and summarize informational videos.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--config-path", required=True, help="path to pipeline config")

    parser.add_argument(
        "--steps",
        nargs="+",  # allows multiple values, e.g. --steps ingest transcribe
        default=["ingest", "transcribe", "summarize"],  # run all by default
        choices=["ingest", "transcribe", "summarize"],  # validate inputs
        help="Pipeline steps to run (default: all). Order matters. Examples:\n"
        "  --steps ingest\n"
        "  --steps ingest transcribe\n"
        "  --steps summarize (skips previous)",
    )

    args = parser.parse_args()
    config = get_pipeline_config(args.config_path)

    url = config["vidoe_url"]
    video_id = get_video_id_from_url(url)
    relic_name = config.get("relic_name", video_id)
    relic_type = config.get("relic_type", "video-summary")

    relic = Relic(
        name=relic_name,
        relic_type=relic_type,
    )

    pipeline = get_pipeline_service(config["pipeline"])
    # Ingestion
    ingestion_result = pipeline.ingest(url)
    ingestion_result["audio"].seek(0)
    relic.add_audio(name="audio.wav", audio_obj=ingestion_result["audio"])
    relic.add_json(name="metadata", json_data=ingestion_result["video_metadata"])
    relic.add_json(name="video_info", json_data=ingestion_result["video_info"])

    # transcription
    ingestion_result["audio"].seek(0)
    transcription = pipeline.transcribe(ingestion_result["audio"])
    readable_transcript = pipeline.get_readable_transcript(transcription)

    relic.add_json(name="vosk-diarized-transcription", json_data=transcription)
    relic.add_text(name="readable-transcript", text=readable_transcript)

    # Summary
    summary = pipeline.summarize(transcript=readable_transcript)

    relic.add_text(name="summary-llm", text=summary)


if __name__ == "__main__":
    main()
