"""Tests for ORP (Optimal Recognition Point) functions."""

from rich.text import Text
from sposa import get_orp_index, format_word_with_orp


class TestGetOrpIndex:
    """Tests for the Optimal Recognition Point calculation."""

    def test_empty_string(self):
        """Empty string should return 0."""
        assert get_orp_index("") == 0

    def test_single_character(self):
        """Single char word: ORP is index 0."""
        assert get_orp_index("a") == 0
        assert get_orp_index("I") == 0

    def test_two_characters(self):
        """Two char word: ORP is index 0 (center-left)."""
        assert get_orp_index("ab") == 0
        assert get_orp_index("is") == 0

    def test_three_characters(self):
        """Three char word: ORP is index 1 (middle)."""
        assert get_orp_index("abc") == 1
        assert get_orp_index("the") == 1

    def test_four_characters(self):
        """Four char word: ORP is index 1 (center-left)."""
        assert get_orp_index("word") == 1
        assert get_orp_index("test") == 1

    def test_five_characters(self):
        """Five char word: ORP is index 2 (middle)."""
        assert get_orp_index("hello") == 2
        assert get_orp_index("world") == 2

    def test_odd_length_word(self):
        """Odd length: should be true center."""
        assert get_orp_index("reading") == 3  # 7 chars, index 3
        assert get_orp_index("example") == 3  # 7 chars, index 3

    def test_even_length_word(self):
        """Even length: should be center-left."""
        assert get_orp_index("python") == 2  # 6 chars, index 2
        assert get_orp_index("sposa") == 2  # 5 chars, index 2

    def test_with_punctuation(self):
        """Punctuation is part of the word."""
        assert get_orp_index("hello,") == 2  # 6 chars, index 2
        assert get_orp_index("world!") == 2  # 6 chars, index 2
        assert get_orp_index("test.") == 2  # 5 chars, index 2


class TestFormatWordWithOrp:
    """Tests for ORP formatting with Rich Text."""

    def test_empty_string(self):
        """Empty string returns empty Text."""
        result = format_word_with_orp("")
        assert isinstance(result, Text)
        assert str(result) == ""

    def test_single_char(self):
        """Single char should be styled."""
        result = format_word_with_orp("a")
        assert str(result) == "a"
        # Check that it has the blue style
        assert len(result.spans) == 1
        assert result.spans[0].style == "#0080ff"

    def test_word_structure(self):
        """Check that word is split correctly: before + ORP + after."""
        result = format_word_with_orp("hello")
        # "hello" has ORP at index 2 ('l')
        # Should be: "he" (plain) + "l" (styled) + "lo" (plain)
        assert str(result) == "hello"
        # Should have at least one styled span for the ORP
        styled_spans = [s for s in result.spans if s.style == "#0080ff"]
        assert len(styled_spans) >= 1

    def test_orp_style_applied(self):
        """ORP letter should have #0080ff style."""
        result = format_word_with_orp("test")
        # Find the styled span
        styled_spans = [s for s in result.spans if s.style == "#0080ff"]
        assert len(styled_spans) == 1

    def test_multiple_words(self):
        """Each word formatted independently."""
        words = ["the", "quick", "brown"]
        results = [format_word_with_orp(w) for w in words]
        assert all(isinstance(r, Text) for r in results)
        assert [str(r) for r in results] == ["the", "quick", "brown"]

    def test_with_punctuation(self):
        """Punctuation preserved in formatted text."""
        result = format_word_with_orp("hello!")
        assert str(result) == "hello!"

        result = format_word_with_orp("world,")
        assert str(result) == "world,"

    def test_two_char_word(self):
        """Two character word formats correctly."""
        result = format_word_with_orp("is")
        assert str(result) == "is"
        # ORP should be at index 0 (the 'i')
        styled_spans = [s for s in result.spans if s.style == "#0080ff"]
        assert len(styled_spans) == 1

    def test_returns_text_object(self):
        """All results should be Rich Text objects."""
        assert isinstance(format_word_with_orp("test"), Text)
        assert isinstance(format_word_with_orp(""), Text)
        assert isinstance(format_word_with_orp("a"), Text)
