import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Set, List, Pattern
import dataclasses
import inspect



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
    _token_re: Pattern[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        print('__post_init__ executed')
        extra = {w.lower() for w in self.extra_stopwords} if self.lowercase else set(self.extra_stopwords)
        self._stopwords = set(STOPWORDS) | extra
        self._token_re = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*") # regular expression pattern that would filter out unnecessary symbols

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


    def generate_wordcloud(self, sentences: List[str]) -> WordCloud:
        # Build word frequencies from the input sentences
        freq = self.frequencies(sentences)

        # Create and generate the word cloud from frequencies
        wc = WordCloud(
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            max_words=self.max_words,
            collocations=self.collocations
        ).generate_from_frequencies(freq)

        return wc


    def show_wordcloud(self, sentences: List[str]) -> WordCloud:
        wc = self.generate_wordcloud(sentences)

        # Display in a new matplotlib window (no file saved)
        plt.figure(figsize=(self.width / 200, self.height / 200))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

        return wc

    def add_stopwords(self, words: set[str]) -> None:
        """
        Add additional stopwords at runtime and update internal stopword set.
        """
        if self.lowercase:
            words = {w.lower() for w in words}

        # Update user-defined stopwords
        self.extra_stopwords |= words

        # Rebuild internal stopwords
        self._stopwords = set(STOPWORDS) | self.extra_stopwords

# ---------- Test ----------
if __name__ == '__main__':
    sentences = [
    "My Long-haired cat -- sleeps on the sofa.",
    "Cats chase laser pointers — and then nap.",
    "A short-haired cat–often sleeps, eats, and plays."
    ]

    gen = Analyzer(extra_stopwords={"cat", "cats"})

    # Test normalization
    print("=== Normalize ===")
    for s in sentences:
        normalized = gen._normalize_text(s)
        print("Original  :", s)
        print("Normalized:", normalized)
        print()

    # Test tokenization
    print("=== Tokenize ===")
    tokens = gen._tokenize(sentences)
    print(tokens)
    print()

    # Test frequencies
    print("=== Frequencies ===")
    freq = gen.frequencies(sentences)
    print(freq)
    print("Most common:", freq.most_common(10))

    gen.show_wordcloud(sentences)