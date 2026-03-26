# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Maps emoji/emoticon tokens to words that exist in POSITIVE_WORDS or NEGATIVE_WORDS,
# so score_text picks them up without any changes.
# Sorted longest-first at use time so ":-)" matches before ":)".
_EMOJI_SENTIMENT: Dict[str, str] = {
    # Text emoticons
    ":-)": "happy",
    ":D":  "happy",
    ":)":  "happy",
    ":-(": "sad",
    ":(":  "sad",
    ":/":  "bad",
    # Unicode emojis
    "😊": "happy",
    "😀": "happy",
    "😁": "happy",
    "😂": "happy",
    "😍": "love",
    "🥲": "sad",
    "😢": "sad",
    "😭": "sad",
    "😡": "angry",
    "😤": "angry",
    "💀": "terrible",
}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        # Step 1: Replace emojis/emoticons with sentiment words before anything
        # else — text emoticons like ":)" are made of punctuation and would be
        # destroyed by the punctuation-removal step below.
        # Sort longest-first so ":-)" matches before ":)".
        cleaned = text.strip()
        for emoji, word in sorted(_EMOJI_SENTIMENT.items(), key=lambda x: -len(x[0])):
            cleaned = cleaned.replace(emoji, f" {word} ")

        # Step 2: Lowercase after emoji replacement so ":D" (happy face) isn't
        # lowercased to ":d" (no match) before we get a chance to replace it.
        cleaned = cleaned.lower()

        # Step 3: Normalize repeated characters so "soooo" → "soo" and
        # "loooove" → "loove". Keeps double letters like "good" intact.
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)

        # Step 4: Remove punctuation. Apostrophes are kept so "don't" stays
        # intact for the negation logic in score_text.
        cleaned = re.sub(r"[^\w\s']", "", cleaned)

        return cleaned.split()

    # ---------------------------------------------------------------------
    # Internal analysis helper
    # ---------------------------------------------------------------------

    _NEGATORS = {"not", "never", "no", "don't", "doesn't", "didn't", "won't", "can't"}

    def _analyze(self, text: str) -> Tuple[int, List[str], List[str]]:
        """
        Core analysis used by score_text, predict_label, and explain.

        Returns (score, positive_hits, negative_hits).
        Negated words (e.g. "not happy") are flipped and recorded with
        their negator so callers can show what actually happened.
        """
        tokens = self.preprocess(text)
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        for i, token in enumerate(tokens):
            is_negated = i > 0 and tokens[i - 1] in self._NEGATORS
            if token in self.positive_words:
                if is_negated:
                    score -= 1
                    negative_hits.append(f"not {token}")
                else:
                    score += 1
                    positive_hits.append(token)
            elif token in self.negative_words:
                if is_negated:
                    score += 1
                    positive_hits.append(f"not {token}")
                else:
                    score -= 1
                    negative_hits.append(token)

        return score, positive_hits, negative_hits

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.
        """
        score, _, _ = self._analyze(text)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score, positive_hits, negative_hits = self._analyze(text)

        # Both sides fired — opposing signals, call it mixed.
        if positive_hits and negative_hits:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        score, positive_hits, negative_hits = self._analyze(text)
        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
