import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class Analyzer:
    """
    This class is designed for generating word cloud from a list of strings.

    Requirements:
        matplotlib, wordcloud
    """
    # ----- Rendering parameters -----
    width: int = 1200 # width of word cloud widget
    height: int = 700 # height of word cloud widget
    background_color: str = "white" # background color of word cloud widget
    max_words: int = 200 # maximum of words shown in word cloud
    collocations: bool = False # Whether to enable automatic detection of common word pairs

    # ----- Text preprocessing parameters -----
    lowercase: bool = True # Whether to convert all text to lowercase
    min_word_length: int = 2 # Minimum length a word must have to be included
    extra_stopwords: Set[str] = field(default_factory=set) # User-defined stopwords (domain-specific high-frequency but meaningless words)

    _stopwords: Set[str] = field(init=False, repr=False) # Final stopwords set actually used during token filtering
    _token_re: re.Pattern = field(init=False, repr=False)

    def __post_init__(self) -> None:
        extra = {w.lower() for w in self._stopwords} if self.lowercase else set(self.extra_stopwords)
        self._stopwords = set(STOPWORDS) | extra
        self._token_re = re.compile(r"[a-z]+(?:-[a-z]+)*") # regular expression pattern that would filter out unnecessary symbols

    def _normalize_text(self, sentence: str) -> str:
        # if self.lowercase == True, merge uppercase/lowercase by converting the entire sentence to lowercase.
        if self.lowercase:
            sentence = sentence.lower()

        # Replace "double-dash" and common dash punctuation with spaces.
        # This removes separators like "--", "—", and "–",
        # while preserving hyphenated words like "long-haired".
        sentence = sentence.replace("--", " ").replace("—", " ").replace("–", " ")

        # Collapse repeated whitespace into a single space and trim ends.
        sentence = re.sub(r"\s+", " ", sentence).strip()

        return sentence

    
    def _tokenize(self, sentences: List[str]) -> List[str]:
        tokens: List[str] = []

        for s in sentences:
            # Normalize each sentence first (case + dash handling + whitespace)
            s = self._normalize_text(s)

            # Extract tokens that match the regex (keeps hyphenated words)
            for tok in self._token_re.findall(s):
                # Filter short tokens
                if len(tok) < self.min_word_length:
                    continue

                # Filter stopwords (built-in + your custom ones)
                if tok in self._stopwords:
                    continue

                tokens.append(tok)

        return tokens

    def frequencies(self, sentences: List[str]) -> Counter:
        tokens = self._tokenize(sentences)
        return Counter(tokens)

if __name__ == '__main__':
    sentences = [
        "My Long-haired cat -- sleeps on the sofa.",
        "Cats chase laser pointers — and then nap.",
        "A short-haired cat–often sleeps, eats, and plays."
    ]

    gen = Analyzer(extra_stopwords={"cat", "cats"})

    # 1) Test normalization
    print("=== Normalize ===")
    for s in sentences:
        print("Original :", s)
        print("Normalized:", gen._normalize_text(s))
        print()

    # 2) Test tokenization
    print("=== Tokenize ===")
    tokens = gen._tokenize(sentences)
    print(tokens)
    print()

    # 3) Test frequencies
    print("=== Frequencies ===")
    freq = gen.frequencies(sentences)
    print(freq)
    print("Most common:", freq.most_common(10))