"""Tests for SposaApp action methods (speed, pause controls)."""

import pytest
from sposa import SposaApp


class TestSpeedControls:
    """Tests for speed control action methods."""

    @pytest.fixture
    def app(self):
        """Create app instance for testing."""
        app = SposaApp()
        # Manually set words (since on_mount won't be called in tests)
        app.words = ["test", "words", "here."]
        return app

    def test_initial_speed_multiplier(self, app):
        """Default speed multiplier is 1.0."""
        assert app.wpm_multiplier == 1.0

    def test_increase_speed(self, app):
        """Increase speed by 0.1."""
        initial = app.wpm_multiplier
        app.action_increase_speed()
        assert app.wpm_multiplier == pytest.approx(initial + 0.1)

    def test_increase_speed_multiple_times(self, app):
        """Increase speed multiple times."""
        app.action_increase_speed()
        app.action_increase_speed()
        app.action_increase_speed()
        assert app.wpm_multiplier == pytest.approx(1.3)

    def test_increase_speed_max_cap(self, app):
        """Speed cannot exceed 2.8x."""
        app.wpm_multiplier = 2.8
        app.action_increase_speed()
        assert app.wpm_multiplier == 2.8

        app.wpm_multiplier = 2.7
        app.action_increase_speed()
        assert app.wpm_multiplier == 2.8

    def test_decrease_speed(self, app):
        """Decrease speed by 0.1."""
        app.wpm_multiplier = 1.5
        app.action_decrease_speed()
        assert app.wpm_multiplier == pytest.approx(1.4)

    def test_decrease_speed_multiple_times(self, app):
        """Decrease speed multiple times."""
        app.wpm_multiplier = 1.5
        app.action_decrease_speed()
        app.action_decrease_speed()
        app.action_decrease_speed()
        assert app.wpm_multiplier == pytest.approx(1.2)

    def test_decrease_speed_min_cap(self, app):
        """Speed cannot go below 0.1x."""
        app.wpm_multiplier = 0.1
        app.action_decrease_speed()
        assert app.wpm_multiplier == 0.1

        app.wpm_multiplier = 0.2
        app.action_decrease_speed()
        assert app.wpm_multiplier == 0.1

    def test_speed_boundaries(self, app):
        """Test speed stays within 0.1 to 2.8 range."""
        # Test minimum
        app.wpm_multiplier = 0.1
        app.action_decrease_speed()
        assert app.wpm_multiplier >= 0.1

        # Test maximum
        app.wpm_multiplier = 2.8
        app.action_increase_speed()
        assert app.wpm_multiplier <= 2.8


class TestPauseToggle:
    """Tests for pause/resume toggle action."""

    @pytest.fixture
    def app(self):
        """Create app instance for testing."""
        app = SposaApp()
        # Manually set words (since on_mount won't be called in tests)
        app.words = ["test", "words", "here."]
        return app

    def test_initial_pause_state(self, app):
        """App starts in paused state."""
        assert app.is_paused is True

    def test_toggle_pause_from_paused(self, app):
        """Toggle from paused to unpaused."""
        app.is_paused = True
        app.current_index = 1
        app.action_toggle_pause()
        assert app.is_paused is False

    def test_toggle_pause_from_playing(self, app):
        """Toggle from playing to paused."""
        app.is_paused = False
        app.current_index = 1
        app.action_toggle_pause()
        assert app.is_paused is True

    def test_toggle_pause_at_end_resets(self, app):
        """At end of text, toggle resets to beginning."""
        app.is_paused = True
        app.current_index = 3  # Beyond words list (has 3 words, indices 0-2)
        app.action_toggle_pause()
        assert app.current_index == 0
        assert app.is_paused is False

    def test_toggle_pause_multiple_times(self, app):
        """Toggle multiple times alternates state."""
        initial_state = app.is_paused
        app.action_toggle_pause()
        assert app.is_paused != initial_state
        app.action_toggle_pause()
        assert app.is_paused == initial_state

    def test_toggle_at_end_with_longer_list(self, app):
        """Test end detection with longer word list."""
        app.words = ["one", "two", "three", "four", "five"]
        app.is_paused = True
        app.current_index = 5  # At end (5 words, indices 0-4)
        app.action_toggle_pause()
        assert app.current_index == 0
        assert app.is_paused is False

    def test_current_index_preserved_when_toggling(self, app):
        """Current index is preserved when toggling mid-reading."""
        app.current_index = 1
        app.is_paused = True
        app.action_toggle_pause()
        assert app.current_index == 1  # Should not change

        app.action_toggle_pause()
        assert app.current_index == 1  # Should not change
