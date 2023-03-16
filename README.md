# Pyannote.audio + Replicate = 💛
This is an implementation of [pyannote.audio](https://github.com/pyannote/pyannote-audio) in a [cog](https://github.com/replicate/cog) wrapper to easily run speaker diarization via [replicate](https://replicate.com/) to save you the trouble of dependency hell 😇.

## How this model works
The model takes an input audio file in the `audio` parameter. Then, it runs speaker diarization and returns a list of audio files containing the individual speaker turns within the audio file split by speaker and index. The output URLs contain encoded information in the file name to make working with the outputs easier. The format for the file name is `{index}_{speaker}_{duration}` which resolves to `0_SPEAKER_01_16`. Duration is in seconds. Index refers to the order of speaker turns.

## Building this model with Cog

1. SSH into a Linux environment with a GPU
1. Install [Cog](https://github.com/replicate/cog#install) (using [replicate/codespaces](https://github.com/replicate/codespaces) if you're using GitHub Codespaces)
1. Create a HuggingFace token and add it to [predict.py](predict.py) as `HUGGINGFACE_TOKEN` (TOOD: Move it out of predict.py somehow.. maybe into a script that caches the weights)
1. Accept license aggrements for these two models on HuggingFace:
  - https://huggingface.co/pyannote/speaker-diarization
  - https://huggingface.co/pyannote/segmentation
1. Run `cog predict -i audio=@example.m4a`

Then:

1. Create a new model at [replicate.com/create](https://replicate.com/create)
1. Run `cog push r8.im/your-username/your-model-name`
