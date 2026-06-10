import csv
import unicodedata

PSV_FILE = "metadata.psv"
DICT_OUT = "grapheme_dict.txt"

# ── Provide your grapheme inventory here ─────────────────────────────────────
GRAPHEMES = [
    # vowels
    "ai", "i", "ii", "u", "uu", "a", "aa",
    # consonants
    "p", "t", "k", "g", "m", "n", "s", "l", "j", "v", "r", "q", "ng", "nng", "h"
]

# Sort longest-first so multigraphs are tried before their component letters
GRAPHEMES_SORTED = sorted(GRAPHEMES, key=len, reverse=True)

oov_chars = set()

def word_to_graphemes(word: str) -> list[str]:
    """Greedily tokenise a word into graphemes (longest match first)."""
    tokens = []
    i = 0
    while i < len(word):
        matched = False
        for g in GRAPHEMES_SORTED:
            if word[i:i + len(g)] == g:
                tokens.append(g)
                i += len(g)
                matched = True
                break
        if not matched:
            oov_chars.add(word[i])
            tokens.append(word[i])
            i += 1
    return tokens

# ── Read words from PSV ───────────────────────────────────────────────────────
words = set()
with open(PSV_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        for word in row["text"].strip().split():
            words.add(word.lower())

# ── Write dictionary ──────────────────────────────────────────────────────────
with open(DICT_OUT, "w", encoding="utf-8") as f:
    for word in sorted(words):
        graphemes = word_to_graphemes(word)
        phones = " ".join(graphemes)
        f.write(f"{word}\t{phones}\n")

print(f"Wrote {len(words)} entries to {DICT_OUT}")

# ── OOV report ────────────────────────────────────────────────────────────────
if oov_chars:
    print(f"\nOOV characters not in grapheme list ({len(oov_chars)} unique):")
    for ch in sorted(oov_chars):
        codepoint = f"U+{ord(ch):04X}"
        name = unicodedata.name(ch, "UNKNOWN")
        print(f"  {ch!r:10} {codepoint}  {name}")
else:
    print("\nNo OOV characters found.")