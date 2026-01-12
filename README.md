# Deepen
### Deepen the conversation.
pulls audio from videos summarizes converstaions condensing long form talks and distilling the most value to be easily consumed.

Deepen processes YouTube podcasts/videos offline on your machine:
- Downloads audio
- Converts to 16kHz mono WAV
- Transcribes with Vosk (lightweight & fully offline)
- Performs speaker diarization with pyannote.audio
- Generates structured JSON turns + human-readable text transcript
- Stores everything via reliquery (local or Google Drive)

Currently focused on local development (Windows/macOS, Python 3.12). GPU acceleration and WhisperX upgrade planned.

## Features

- 100% offline after initial model downloads
- No cloud dependency for core processing
- Speaker-aware turns with timestamps
- Readable .txt transcript output
- reliquery artifact storage (local + optional Google Drive/S3/Dropbox)

## Requirements

- Python 3.12 (mamba recommended)
- FFmpeg (for audio conversion) — installed via conda
- NVIDIA GPU (optional, for future WhisperX)
- Hugging Face account (free token for pyannote)

## Installation & Dev Setup

### 1. Create conda environment (recommended)
Using `mamba` for `conda` related installs is recommendeded. Same goes for `uv` realeted to `pip`.

```bash
mamba env create -f environment.yml

uv pip install -r requirements.txt
```
After the environement is setup it's time to download vosk models.

### 3. Model Setup (One-time Downloads)

Vosk models are downloaded **once** and used **fully offline** forever. No internet required after initial setup.

#### Vosk (English small model – ~50 MB)
1. Go to the official Vosk models page:  
   https://alphacephei.com/vosk/models  
2. Download **vosk-model-small-en-us-0.15** (recommended for speed and good accuracy on podcasts/interviews).  
   - Alternative: `vosk-model-en-us-0.22` (larger, slightly better accuracy, ~1.5 GB)  
3. Extract the zip file to a folder at the deepen root.
4. Note the **full path** to the extracted folder — you'll add it to your `config.json` (see Configuration section).

## Configuration & Setup

Deepen uses a simple `config.json` file in the project root to store model paths, secrets, and pipeline defaults.  

### Step-by-Step Setup

1. Create a new file named `config.json` in the root of the project.
2. Copy the example below and paste it into the file.
3. Fill in your actual values:
   - Replace the Vosk path with the **full path** to your downloaded and extracted Vosk model folder.
   - Replace the `hf_token` with your real Hugging Face read token (see Model Setup section for how to get one).
   - Customize any other fields as needed (e.g., different Ollama model).
4. Save the file — Deepen will load it automatically.

### Example config.json

```json
{
  "pipeline": {
    "ingestion": {},
    "transcription": {
      "models": {
        "pyannote": "pyannote/speaker-diarization-3.1",
        "vosk": "vosk_models/en-us-medium"
      },
      "secrets": {
        "hf_token": "hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      }
    },
    "summarization": {
      "models": {
        "llama": "llama3.1"
      }
    }
  },
  "video_url": "https://www.youtube.com/watch?v=YRMVTmbe-Is",
  "relic_name": "youtube-deepen",
  "relic_type": "dialogue-summary"
}
```

### Run Deepen Pipeline

Run deepen pipeline on a terminal like so:
```
python deepen.py --config-path config.json
```

