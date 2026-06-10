# Aligner

## Prerequisites

Install [Miniforge](https://github.com/conda-forge/miniforge) if you don't already have conda.

## Installation

```bash
conda config --add channels conda-forge
conda create -n aligner montreal-forced-aligner
conda activate aligner
mfa --help
```

## Training

Data must go in `data` with speakers separated. 

```
data/
  speaker/
    Speaker_utterance.wav
    Speaker_utterance.txt
```

You can build this from a metadata.psv file and a wavs folder using `scripts/data_builder.py`

### Build the dict

The dictionary takes a tsv file with a word in column 1 and a space-separated list of alignable units (i.e. phonemes) in column 2:

```tsv
hello h e l l o
```

or

```tsv
hello h ə l o ʊ
```


You can build a character-level dictionary from a metadata.psv file with `scripts/dict_builder-character.py`. You can build a grapheme-level dictionary (digraphs/multigraphs supported) with `scripts/dict_builder-grapheme.py`

### Train

Then you can run training with: 

`mfa train <PATH_TO_MFA_FORMAT_CORPUS> <PATH_TO_DICT.txt> model.zip --output_directory alignments --clean --jobs <CPU_COUNT>`

## Inference

After you've trained a model, you can run inference on new segments with the following:

### Input format

Audio and transcript files go in `to_align/`. Each pair must share the same base name:

```
to_align/
  Speaker_utterance.wav
  Speaker_utterance.txt
```

### Adding new words

Before aligning, any words not already in `character_dict.txt` must be added.

### Aligning

```bash
mfa align \
  to_align/ \
  character_dict.txt \
  models/my_char_aligner.zip \
  aligned/ \
  --clean
```

### Output

Aligned TextGrids are written to `aligned/`. Open them in [Praat](https://www.fon.hum.uva.nl/praat/).

#### Demo app

To see the alignments without using Praat, you can use the following web app.

```bash
uv sync
uv run python app.py
```

Then open http://localhost:8080.

#### Parsing with Python

```bash
pip install praatio
```

```python
from praatio import textgrid

tg = textgrid.openTextgrid("aligned/Speaker_utterance.TextGrid", includeEmptyIntervals=False)
for tier_name in tg.tierNames:
    tier = tg.getTier(tier_name)
    for entry in tier.entries:
        print(f"{tier_name}  {entry.start:.3f} – {entry.end:.3f}  {entry.label}")
```
