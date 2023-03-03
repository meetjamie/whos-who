# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path, File, BaseModel
import os
import subprocess
from typing import List
from pyannote.audio import Pipeline
from pydub import AudioSegment
import re
import subprocess
import datetime

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="yourToken")

    def predict(
        self,,
        audio: Path = Input(description="Audio file in most common audio formats"),
    ) -> List[Path]:
        """Run a single prediction on the model"""

        # convert input file to wav
        convert_to_wav(audio, "convertedAudio.wav")

        # pyannote seems to miss first 0.5 seconds, hence prepending a spacer
        spacermilli = 2000
        spacer = AudioSegment.silent(duration=spacermilli)
        audio = AudioSegment.from_wav("convertedAudio.wav")
        audio = spacer.append(audio, crossfade=0)
        audio.export('adjustedAudio.wav', format='wav')

        # assuming number of speakers is not given, automatic detection
        print("starting diarization of file")
        try:
            dz = self.pipeline("adjustedAudio.wav")
        except ValueError:
            # audio chunk must have been empty (without voice)
            return False
        # else:
          #  dz = self.pipeline("adjustedAudio.wav", num_speakers=numberSpeakers)
        # process file in pipeline with pyannote
        
        # saving diarization to file
        with open("diarization.txt", "w") as text_file:
            text_file.write(str(dz))
        
        # preparing audio files for each diariation turn
        def millisec(timeStr):
            spl = timeStr.split(":")
            s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
            return s


        dzs = open('diarization.txt').read().splitlines()

        groups = []
        g = []
        lastend = 0

        # this groups diarization turns by speakers in sequence (=when there are >1 consecutive turns by the same speaker)
        for d in dzs:   
            if g and (g[0].split()[-1] != d.split()[-1]): #same speaker
                groups.append(g)
                g = []
            
            g.append(d)
            
            end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
            end = millisec(end)
            if (lastend > end):       #segment engulfed by a previous segment
                groups.append(g)
                g = [] 
            else:
                lastend = end
        if g:
            groups.append(g)
            print(*groups, sep='\n')

        
        # creating & saving corresponding audio parts
        audioFile = AudioSegment.from_wav("adjustedAudio.wav")
        gidx = -1
        output = []
        for g in groups:
            # get start and end time
            start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
            end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
            start = millisec(start) #- spacermilli
            end = millisec(end)  #- spacermilli
            # print(start, end)

            # get duration of audio segment
            duration = end - start
            if duration < 2 * 1000:  # 2 seconds in milliseconds
                continue  # skip this iteration if duration is too short

            roundedDuration = round(duration / 1000)

            # get speaker
            match = re.search(r"SPEAKER_\d+", g[0])
            speaker = match.group()

            gidx += 1
            path = str(audioChunkIndex) + "_" + str(gidx) + "_" + str(speaker) + "_" + str(roundedDuration) +'.wav'

            audioFile[start:end].export(path, format='wav')
            output.append(Path(path))

        # returning results
        return output

def convert_to_wav(input_file, output_file):
    # Check if input file exists
    if not os.path.isfile(input_file):
        raise ValueError(f"Input file {input_file} does not exist")

    # Use ffmpeg to convert the input file to WAV format
    subprocess.run(["ffmpeg", "-i", input_file, "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", output_file])

    # Check if output file was created
    if not os.path.isfile(output_file):
        raise RuntimeError("Failed to create output file")

    print(f"Successfully converted {input_file} to {output_file}")
