import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Set


@dataclass
class Analyzer:
    # ----- Rendering parameters -----
    width: int = 1200
    height: int = 700
    background_color: str = "white"
    max_words: int = 200
    collocations: bool = False

    # ----- Text preprocessing parameters -----
    lowercase: bool = True
    min_word_length: int = 2
    extra_stopwords: Set[str] = field(default_factory=set)
