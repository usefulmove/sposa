"""Tests for file loading functionality."""

import pytest
from pathlib import Path
from sposa import load_words_from_file


class TestFileLoading:
    """Tests for load_words_from_file function."""

    def test_load_simple_file(self, temp_text_file):
        """Load a simple text file."""
        test_file = temp_text_file("Hello World")

        words = load_words_from_file(test_file)
        assert words == ["hello", "world"]

    def test_load_multiline_file(self, temp_text_file):
        """Load file with multiple lines."""
        test_file = temp_text_file("Line one\nLine two\nLine three")

        words = load_words_from_file(test_file)
        assert words == ["line", "one", "line", "two", "line", "three"]

    def test_load_file_with_punctuation(self, temp_text_file):
        """Punctuation is preserved."""
        test_file = temp_text_file("Hello, world! How are you?")

        words = load_words_from_file(test_file)
        assert words == ["hello,", "world!", "how", "are", "you?"]

    def test_load_file_with_extra_whitespace(self, temp_text_file):
        """Extra whitespace is normalized."""
        test_file = temp_text_file("  spaced    text   here  ")

        words = load_words_from_file(test_file)
        assert words == ["spaced", "text", "here"]

    def test_load_file_with_tabs_and_newlines(self, temp_text_file):
        """Tabs and newlines are treated as whitespace."""
        test_file = temp_text_file("word1\tword2\nword3\r\nword4")

        words = load_words_from_file(test_file)
        assert words == ["word1", "word2", "word3", "word4"]

    def test_load_empty_file(self, temp_text_file):
        """Empty file returns empty list."""
        test_file = temp_text_file("")

        words = load_words_from_file(test_file)
        assert words == []

    def test_load_whitespace_only_file(self, temp_text_file):
        """File with only whitespace returns empty list."""
        test_file = temp_text_file("   \n\t  \n  ")

        words = load_words_from_file(test_file)
        assert words == []

    def test_load_file_not_found(self):
        """Non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_words_from_file("/nonexistent/file.txt")

    def test_load_file_converts_to_lowercase(self, temp_text_file):
        """All words are converted to lowercase."""
        test_file = temp_text_file("UPPER lower MiXeD")

        words = load_words_from_file(test_file)
        assert words == ["upper", "lower", "mixed"]
        # Verify all are lowercase
        assert all(w == w.lower() for w in words)

    def test_load_file_preserves_punctuation_case(self, temp_text_file):
        """Lowercase conversion preserves punctuation."""
        test_file = temp_text_file("Hello, WORLD! What's UP?")

        words = load_words_from_file(test_file)
        assert words == ["hello,", "world!", "what's", "up?"]

    def test_load_actual_fixture_simple(self):
        """Load from actual test fixture: simple.txt."""
        fixture_path = Path("tests/fixtures/simple.txt")
        words = load_words_from_file(str(fixture_path))
        assert isinstance(words, list)
        assert words == ["hello", "world"]

    def test_load_actual_fixture_punctuated(self):
        """Load from actual test fixture: punctuated.txt."""
        fixture_path = Path("tests/fixtures/punctuated.txt")
        words = load_words_from_file(str(fixture_path))
        assert isinstance(words, list)
        assert words == ["hello,", "world!", "how", "are", "you?"]

    def test_load_actual_fixture_empty(self):
        """Load from actual test fixture: empty.txt."""
        fixture_path = Path("tests/fixtures/empty.txt")
        words = load_words_from_file(str(fixture_path))
        assert words == []

    def test_load_actual_fixture_multisentence(self):
        """Load from actual test fixture: multisentence.txt."""
        fixture_path = Path("tests/fixtures/multisentence.txt")
        words = load_words_from_file(str(fixture_path))
        assert isinstance(words, list)
        assert len(words) > 0
        assert all(isinstance(w, str) for w in words)
        # Verify lowercase
        assert all(w == w.lower() for w in words if w.isalpha())

    def test_load_returns_list_of_strings(self, temp_text_file):
        """Function returns a list of strings."""
        test_file = temp_text_file("test words here")
        words = load_words_from_file(test_file)
        assert isinstance(words, list)
        assert all(isinstance(w, str) for w in words)

    def test_load_file_with_numbers(self, temp_text_file):
        """Numbers are treated as words."""
        test_file = temp_text_file("word1 123 word2 456.789")
        words = load_words_from_file(test_file)
        assert words == ["word1", "123", "word2", "456.789"]
