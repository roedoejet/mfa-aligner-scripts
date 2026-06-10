import csv
import unicodedata

PSV_FILE = "metadata.psv"
DICT_OUT = "character_dict.txt"

words = set()
with open(PSV_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        for word in row["text"].strip().split():
            words.add(word.lower())  # normalise case if needed

with open(DICT_OUT, "w", encoding="utf-8") as f:
    for word in sorted(words):
        phones = " ".join(list(word))   # each char = one phone
        f.write(f"{word}\t{phones}\n")

print(f"Wrote {len(words)} entries to {DICT_OUT}")
