"""Shared pytest fixtures for Sposa tests."""

import pytest


@pytest.fixture
def temp_text_file(tmp_path):
    """Create temporary text files for testing.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        A function that creates a text file with given content
    """

    def _make_file(content: str, filename: str = "test.txt") -> str:
        file_path = tmp_path / filename
        file_path.write_text(content)
        return str(file_path)

    return _make_file


@pytest.fixture
def sample_words():
    """Provide sample word lists for testing.

    Returns:
        A dictionary of sample word lists for different test scenarios
    """
    return {
        "simple": ["hello", "world"],
        "punctuated": ["hello.", "how", "are", "you?"],
        "sentences": ["first", "one.", "second", "here!", "third", "now?"],
        "empty": [],
    }
