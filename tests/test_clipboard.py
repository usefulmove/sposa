"""Tests for clipboard functionality and argument parsing."""

import sys
from unittest.mock import patch

import pytest

from sposa import (
    load_text_from_clipboard,
    load_words_from_text,
    parse_arguments,
)


class TestLoadWordsFromText:
    """Tests for load_words_from_text helper function."""

    def test_simple_text(self):
        """Simple text is split into words."""
        text = "Hello World"
        words = load_words_from_text(text)
        assert words == ["hello", "world"]

    def test_multiline_text(self):
        """Newlines are treated as whitespace."""
        text = "Line one\nLine two\nLine three"
        words = load_words_from_text(text)
        assert words == ["line", "one", "line", "two", "line", "three"]

    def test_empty_text(self):
        """Empty text returns empty list."""
        words = load_words_from_text("")
        assert words == []

    def test_whitespace_only(self):
        """Whitespace-only text returns empty list."""
        text = "   \n\t  \n  "
        words = load_words_from_text(text)
        assert words == []

    def test_punctuation_preserved(self):
        """Punctuation is preserved in words."""
        text = "Hello, world! How are you?"
        words = load_words_from_text(text)
        assert words == ["hello,", "world!", "how", "are", "you?"]

    def test_case_normalization(self):
        """Text is lowercased."""
        text = "UPPER lower MiXeD"
        words = load_words_from_text(text)
        assert words == ["upper", "lower", "mixed"]


class TestLoadTextFromClipboard:
    """Tests for load_text_from_clipboard function."""

    @patch("pyperclip.paste")
    def test_success(self, mock_paste):
        """Normal text loading from clipboard."""
        mock_paste.return_value = "Hello World"
        text = load_text_from_clipboard()
        assert text == "Hello World"
        mock_paste.assert_called_once()

    @patch("pyperclip.paste")
    def test_multiline_text(self, mock_paste):
        """Multiline text is preserved."""
        mock_paste.return_value = "Line 1\nLine 2\nLine 3"
        text = load_text_from_clipboard()
        assert text == "Line 1\nLine 2\nLine 3"

    @patch("pyperclip.paste")
    def test_with_punctuation(self, mock_paste):
        """Punctuation is preserved."""
        mock_paste.return_value = "Hello, world! How are you?"
        text = load_text_from_clipboard()
        assert text == "Hello, world! How are you?"

    @patch("pyperclip.paste")
    def test_empty_clipboard(self, mock_paste):
        """Empty clipboard raises ValueError."""
        mock_paste.return_value = ""
        with pytest.raises(ValueError, match="Clipboard is empty"):
            load_text_from_clipboard()

    @patch("pyperclip.paste")
    def test_whitespace_only_clipboard(self, mock_paste):
        """Whitespace-only clipboard raises ValueError."""
        mock_paste.return_value = "   \n\t  \n  "
        with pytest.raises(ValueError, match="Clipboard is empty"):
            load_text_from_clipboard()

    @patch("pyperclip.paste")
    def test_clipboard_unavailable(self, mock_paste):
        """Clipboard access failure raises RuntimeError."""
        mock_paste.side_effect = Exception("No clipboard available")
        with pytest.raises(RuntimeError, match="Failed to access clipboard"):
            load_text_from_clipboard()

    @patch("pyperclip.paste")
    def test_lowercasing_happens_later(self, mock_paste):
        """Case is preserved in clipboard text (lowercasing in load_words_from_text)."""
        mock_paste.return_value = "UPPER lower MiXeD"
        text = load_text_from_clipboard()
        assert text == "UPPER lower MiXeD"  # Not lowercased yet

    @patch("pyperclip.paste")
    def test_word_splitting_happens_later(self, mock_paste):
        """Text remains as single string (splitting in load_words_from_text)."""
        mock_paste.return_value = "Multiple words here"
        text = load_text_from_clipboard()
        assert isinstance(text, str)
        assert text == "Multiple words here"


class TestParseArguments:
    """Tests for parse_arguments function."""

    def test_file_argument(self):
        """File path is parsed correctly."""
        with patch.object(sys, "argv", ["sposa", "myfile.txt"]):
            source_type, filename = parse_arguments()
            assert source_type == "file"
            assert filename == "myfile.txt"

    def test_clipboard_keyword_lowercase(self):
        """':clipboard:' keyword is recognized."""
        with patch.object(sys, "argv", ["sposa", ":clipboard:"]):
            source_type, filename = parse_arguments()
            assert source_type == "clipboard"
            assert filename is None

    def test_clipboard_keyword_uppercase(self):
        """':CLIPBOARD:' (uppercase) is recognized."""
        with patch.object(sys, "argv", ["sposa", ":CLIPBOARD:"]):
            source_type, filename = parse_arguments()
            assert source_type == "clipboard"
            assert filename is None

    def test_clipboard_keyword_mixed_case(self):
        """':ClipBoard:' (mixed case) is recognized."""
        with patch.object(sys, "argv", ["sposa", ":ClipBoard:"]):
            source_type, filename = parse_arguments()
            assert source_type == "clipboard"
            assert filename is None

    def test_clipboard_flag(self):
        """'--clipboard' flag is recognized."""
        with patch.object(sys, "argv", ["sposa", "--clipboard"]):
            source_type, filename = parse_arguments()
            assert source_type == "clipboard"
            assert filename is None

    def test_clipboard_both_keyword_and_flag(self):
        """Both keyword and flag defaults to clipboard."""
        with patch.object(sys, "argv", ["sposa", "--clipboard", ":clipboard:"]):
            source_type, filename = parse_arguments()
            assert source_type == "clipboard"
            assert filename is None

    def test_no_arguments(self):
        """No arguments exits with code 0 and shows help."""
        with patch.object(sys, "argv", ["sposa"]):
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
            assert exc_info.value.code == 0

    def test_file_with_spaces(self):
        """File path with spaces is handled correctly."""
        with patch.object(sys, "argv", ["sposa", "my file.txt"]):
            source_type, filename = parse_arguments()
            assert source_type == "file"
            assert filename == "my file.txt"

    def test_file_with_path(self):
        """File with path is handled correctly."""
        with patch.object(sys, "argv", ["sposa", "reads/meditations"]):
            source_type, filename = parse_arguments()
            assert source_type == "file"
            assert filename == "reads/meditations"

    def test_returns_correct_types(self):
        """Return types are correct."""
        with patch.object(sys, "argv", ["sposa", "test.txt"]):
            result = parse_arguments()
            assert isinstance(result, tuple)
            assert len(result) == 2
            source_type, filename = result
            assert source_type in ("file", "clipboard")
            assert isinstance(filename, str) or filename is None


class TestClipboardIntegration:
    """Integration tests for clipboard and text processing."""

    @patch("pyperclip.paste")
    def test_clipboard_to_words_pipeline(self, mock_paste):
        """Full pipeline from clipboard to word list."""
        mock_paste.return_value = "Hello World Test"
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert words == ["hello", "world", "test"]

    @patch("pyperclip.paste")
    def test_clipboard_with_punctuation_pipeline(self, mock_paste):
        """Pipeline preserves punctuation."""
        mock_paste.return_value = "Hello, world! How are you?"
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert words == ["hello,", "world!", "how", "are", "you?"]

    @patch("pyperclip.paste")
    def test_clipboard_multiline_pipeline(self, mock_paste):
        """Pipeline handles multiline text."""
        mock_paste.return_value = "Line 1\nLine 2\nLine 3"
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert words == ["line", "1", "line", "2", "line", "3"]

    @patch("pyperclip.paste")
    def test_large_clipboard_content(self, mock_paste):
        """Large clipboard content is handled."""
        # Create ~1000 words
        large_text = " ".join([f"word{i}" for i in range(1000)])
        mock_paste.return_value = large_text
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert len(words) == 1000
        assert words[0] == "word0"
        assert words[999] == "word999"

    @patch("pyperclip.paste")
    def test_unicode_characters(self, mock_paste):
        """Unicode characters are preserved."""
        mock_paste.return_value = "café résumé naïve"
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert words == ["café", "résumé", "naïve"]

    @patch("pyperclip.paste")
    def test_numbers_and_special_chars(self, mock_paste):
        """Numbers and special characters work."""
        mock_paste.return_value = "test123 $100 @user #hashtag"
        text = load_text_from_clipboard()
        words = load_words_from_text(text)
        assert words == ["test123", "$100", "@user", "#hashtag"]
