import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Set


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

    def __post_init__(self) -> None:
        extra = {w.lower() for w in self._stopwords} if self.lowercase else set(self.extra_stopwords)
        self._stopwords = set(STOPWORDS) | extra

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
