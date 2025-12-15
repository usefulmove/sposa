"""Tests for sentence navigation functions."""

import pytest
from sposa import SposaApp


class TestSentenceNavigation:
    """Tests for sentence finding logic."""

    @pytest.fixture
    def app_with_words(self):
        """Create app instance with test words."""
        app = SposaApp()
        # Don't run the app, just set up words for testing
        return app

    def test_find_sentence_start_at_beginning(self, app_with_words):
        """First sentence starts at index 0."""
        app_with_words.words = ["hello", "world."]
        assert app_with_words._find_sentence_start(0) == 0
        assert app_with_words._find_sentence_start(1) == 0

    def test_find_sentence_start_with_period(self, app_with_words):
        """Find sentence start after period."""
        app_with_words.words = ["hello", "world.", "new", "sentence."]
        # From index 2 (word "new"), should find start at 2
        assert app_with_words._find_sentence_start(2) == 2
        # From index 3, should find start at 2
        assert app_with_words._find_sentence_start(3) == 2

    def test_find_sentence_start_with_question(self, app_with_words):
        """Question mark is a sentence boundary."""
        app_with_words.words = ["what", "time?", "now", "please."]
        assert app_with_words._find_sentence_start(2) == 2  # "now"
        assert app_with_words._find_sentence_start(3) == 2  # "please"

    def test_find_sentence_start_with_exclamation(self, app_with_words):
        """Exclamation mark is a sentence boundary."""
        app_with_words.words = ["stop!", "wait", "here."]
        assert app_with_words._find_sentence_start(1) == 1  # "wait"
        assert app_with_words._find_sentence_start(2) == 1  # "here"

    def test_find_sentence_start_no_punctuation(self, app_with_words):
        """No sentence boundaries returns 0."""
        app_with_words.words = ["no", "punctuation", "here"]
        assert app_with_words._find_sentence_start(2) == 0

    def test_find_sentence_start_at_zero(self, app_with_words):
        """At index 0, should return 0."""
        app_with_words.words = ["first", "word."]
        assert app_with_words._find_sentence_start(0) == 0

    def test_find_next_sentence_start_basic(self, app_with_words):
        """Find start of next sentence."""
        app_with_words.words = ["hello", "world.", "new", "sentence."]
        # From index 0, should find next at 2
        assert app_with_words._find_next_sentence_start(0) == 2
        # From index 1, should find next at 2
        assert app_with_words._find_next_sentence_start(1) == 2

    def test_find_next_sentence_at_end(self, app_with_words):
        """At last sentence, should return last index."""
        app_with_words.words = ["hello", "world."]
        # From index 1 (already at end), should return 1
        assert app_with_words._find_next_sentence_start(1) == 1

    def test_find_next_sentence_no_more_sentences(self, app_with_words):
        """No more sentences returns last index."""
        app_with_words.words = ["only", "one", "sentence"]
        assert app_with_words._find_next_sentence_start(0) == 2

    def test_sentence_navigation_with_mixed_punctuation(self, app_with_words):
        """Multiple sentence types."""
        app_with_words.words = [
            "first",
            "sentence.",
            "second",
            "one?",
            "third",
            "here!",
        ]
        # Sentence starts: 0, 2, 4
        assert app_with_words._find_sentence_start(1) == 0
        assert app_with_words._find_sentence_start(3) == 2
        assert app_with_words._find_sentence_start(5) == 4

        assert app_with_words._find_next_sentence_start(0) == 2
        assert app_with_words._find_next_sentence_start(2) == 4

    def test_find_sentence_start_multiple_sentences(self, app_with_words):
        """Navigate through multiple sentences."""
        app_with_words.words = ["one.", "two.", "three.", "four."]
        # Each word is its own sentence
        assert app_with_words._find_sentence_start(0) == 0
        assert app_with_words._find_sentence_start(1) == 1
        assert app_with_words._find_sentence_start(2) == 2
        assert app_with_words._find_sentence_start(3) == 3

    def test_find_next_sentence_from_middle(self, app_with_words):
        """Find next sentence from middle of current sentence."""
        app_with_words.words = ["this", "is", "sentence", "one.", "next", "here."]
        # From word at index 2, should find next sentence at 4
        assert app_with_words._find_next_sentence_start(2) == 4
