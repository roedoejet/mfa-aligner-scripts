import csv
import os
import shutil

PSV_FILE = "metadata.psv" # bn has .wav at end
WAV_DIR  = "wavs"
OUT_DIR  = "mfa_corpus"

with open(PSV_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        basename   = row["basename"].strip()
        text       = row["text"].strip()
        speaker_id = row["speaker"].strip()

        spk_dir = os.path.join(OUT_DIR, speaker_id)
        os.makedirs(spk_dir, exist_ok=True)

        # Copy wav
        src_wav = os.path.join(WAV_DIR, basename)
        dst_wav = os.path.join(spk_dir, basename)
        shutil.copy2(src_wav, dst_wav)

        # Write lab
        with open(os.path.join(spk_dir, basename[:-4] + ".lab"), "w", encoding="utf-8") as lab:
            lab.write(text + "\n")
