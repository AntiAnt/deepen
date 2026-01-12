from io import BytesIO
from typing import Dict, List

from ingestion.ingestion import get_ingestion_service
from summary.summary import get_summary_service
from transcription.transcription import get_transcription_service


class DeepenPipeline:
    def __init__(
        self,
        ingestion_serivce=None,
        transcription_service=None,
        summary_service=None,
    ):
        self.ingestion_service = ingestion_serivce
        self.transcription_service = transcription_service
        self.summary_service = summary_service

    def ingest(self, url) -> Dict:
        return self.ingestion_service.ingest_audio(url)

    def transcribe(self, audio: BytesIO) -> List[Dict]:
        return self.transcription_service.transcribe(audio)

    def get_readable_transcript(
        self, transcript: List | Dict
    ) -> (
        str
    ):  # TODO add a transcription map so in the config we can assign a name to the speker and keep track.
        return self.transcription_service.get_readable_transcript(transcript)

    def summarize(self, transcript: str) -> str:
        return self.summary_service.summarize(transcript=transcript)


def get_pipeline_service(config: Dict):
    ingestion_service = get_ingestion_service()
    transcription_service = get_transcription_service(config["transcription"])
    summary_service = get_summary_service(config["summarization"])
    return DeepenPipeline(
        ingestion_serivce=ingestion_service,
        transcription_service=transcription_service,
        summary_service=summary_service,
    )
