# Pyannote.audio + Replicate = 💛
This is an implementation of [pyannote.audio](https://github.com/pyannote/pyannote-audio) in a [cog](https://github.com/replicate/cog) wrapper to easily run speaker diarization via [replicate](https://replicate.com/) to save you the trouble of dependency hell 😇.


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
