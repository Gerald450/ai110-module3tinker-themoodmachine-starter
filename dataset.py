"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # Added posts
    "Lowkey stressed but no cap kinda proud of myself",        # slang, mixed
    "I absolutely love being stuck in traffic for two hours",  # sarcasm
    "just vibing 😊",                                         # slang + emoji
    "this homework is killing me 💀",                         # slang + emoji
    "highkey obsessed with this new song",                    # slang
    "I'm fine. Everything is fine. 🙂",                       # sarcasm/ambiguous
    "feeling 🥲 rn but at least it's Friday",                 # emoji, mixed
    "got the job!!! 😂😂 no way this is real",                # emoji, positive
    "another Monday. cool. great. love that for me.",         # sarcasm
    "not sad just tired and empty lol",                       # ambiguous/negative
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # Added labels
    "mixed",     # lowkey stressed but proud — competing feelings
    "negative",  # sarcasm — clearly hates being in traffic
    "positive",  # just vibing with a smile emoji
    "negative",  # "killing me" even as hyperbole reads as overwhelmed
    "positive",  # highkey obsessed = strong enthusiasm
    "mixed",     # forced smile emoji hints at masking feelings
    "mixed",     # sad emoji but a silver lining (Friday)
    "positive",  # genuine excitement about good news
    "negative",  # sarcastic take on Mondays
    "negative",  # explicitly denies sadness but describes it anyway
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
