#!/usr/bin/env python
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ProgressBar
from textual.containers import Container, Vertical
from textual.reactive import reactive
from rich.text import Text
import sys


def main() -> None:
    """Run the Sposa TUI app."""
    app = SposaApp()
    app.run()


def get_orp_index(word: str) -> int:
    """Calculate the Optimal Recognition Point (ORP) index for a word.

    The ORP is the center letter of the word, which is where the eye
    naturally focuses for fastest recognition.

    Args:
        word: The word to calculate ORP for.

    Returns:
        The index of the ORP letter (0-based).
    """
    if not word:
        return 0
    return (len(word) - 1) // 2


def format_word_with_orp(word: str) -> Text:
    """Format a word with the ORP letter dimmed.

    Args:
        word: The word to format.

    Returns:
        A Rich Text object with the ORP letter formatted.
    """
    if not word:
        return Text("")

    orp_idx = get_orp_index(word)
    text = Text()

    # Add characters before ORP
    if orp_idx > 0:
        text.append(word[:orp_idx])

    # Add the ORP letter (highlighted)
    text.append(word[orp_idx], style="#0080ff")

    # Add characters after ORP
    if orp_idx < len(word) - 1:
        text.append(word[orp_idx + 1 :])

    return text


def load_words_from_file(filename: str) -> list[str]:
    """Load and process words from a file.

    Args:
        filename: Path to the text file to load.

    Returns:
        List of lowercase words from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(filename, "r") as file:
        return [word.lower() for word in file.read().split()]


class SposaApp(App):
    """A Textual app for RSVP reading."""

    TITLE = "Sposa"
    ENABLE_COMMAND_PALETTE = False

    CSS = """
    /* Catppuccin Mocha Theme */
    $base: #191724;
    $text: #cdd6f4;
    $mauve: #cba6f7;
    $surface0: #191724;
    $overlay0: #444155;
    $red: #f38ba8;
    $green: #a6e3a1;
    $lavender: #b4befe;
    $blue: #89b4fa;

    Screen {
        align: center middle;
        background: $base;
        color: $text;
    }

    #display-container {
        width: 100%;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background: $base;
    }

    #reader-display {
        text-align: center;
        content-align: center middle;
        width: 100%;
        color: $text;
        height: auto;
    }
    
    #bottom-section {
        dock: bottom;
        height: 3;
        width: 100%;
    }

    #speed-indicator {
        height: 1;
        width: 100%;
        content-align: center middle;
        color: $overlay0;
        text-align: center;
        background: $surface0;
    }

    ProgressBar {
        width: 100%;
        height: 1;
    }
    
    Bar {
        width: 100%;
        background: $surface0;
    }
    
    Bar > .bar--bar {
        color: $mauve;
        background: $overlay0;
    }
    
    Bar > .bar--complete {
        color: $overlay0;
        background: $surface0;
    }
    
    Bar > .bar--indeterminate {
        color: $mauve;
        background: $surface0;
    }

    #bottom-section Footer {
        height: 1;
    }

    Footer {
        background: $surface0;
        color: $lavender;
        dock: bottom;
        align-horizontal: center;
    }
    
    Footer > .footer--key {
        background: $surface0;
        color: $lavender;
    }
    
    Footer > .footer--description {
        color: $overlay0;
    }
    """

    BINDINGS = [
        ("q", "quit", "quit"),
        ("space", "toggle_pause", "play/pause"),
        ("up", "increase_speed", "faster"),
        ("down", "decrease_speed", "slower"),
        ("left", "prev_sentence", "back"),
        ("right", "next_sentence", "forward"),
        ("h", "prev_sentence", None),
        ("l", "next_sentence", None),
        ("k", "increase_speed", None),
        ("j", "decrease_speed", None),
    ]

    # Reactive state
    display_text: reactive[Text] = reactive(Text)
    is_paused: reactive[bool] = reactive(True)
    wpm_multiplier: reactive[float] = reactive(1.0)
    current_index: reactive[int] = reactive(0)

    # Internal state
    words: list[str] = []

    def __init__(self, words: list[str] | None = None):
        """Initialize the Sposa app.

        Args:
            words: Optional pre-loaded word list for testing.
                   If None, words will be loaded from file in on_mount.
        """
        super().__init__()
        self._initial_words = words

    def on_mount(self) -> None:
        """Load content and start the reader."""
        if self._initial_words is not None:
            # Use pre-loaded words (for testing)
            self.words = self._initial_words
        else:
            # Load from file via command line
            try:
                filename = sys.argv[1]
                self.words = load_words_from_file(filename)
            except (IndexError, FileNotFoundError):
                self.words = [
                    "sposa.",
                    "ready",
                    "to",
                    "read.",
                    "please",
                    "provide",
                    "a",
                    "file.",
                ]

        if self.words:
            self.display_text = format_word_with_orp(self.words[0])

        self.query_one(ProgressBar).total = len(self.words)
        self.run_reader()

    def run_reader(self) -> None:
        """Start the reading loop."""
        if not self.words:
            return

        # Start the recursive update loop
        self.set_timer(0.1, self.process_step)

    def process_step(self) -> None:
        """The main loop for the reader."""
        if self.is_paused:
            # Check again in 100ms if paused
            self.set_timer(0.1, self.process_step)
            return

        if self.current_index >= len(self.words):
            self.is_paused = True
            self.set_timer(0.1, self.process_step)
            return

        word = self.words[self.current_index]
        self.animate_typing(word)

    def animate_typing(self, word: str, char_idx: int = 1) -> None:
        """Recursive typing effect."""
        if self.is_paused:
            self.set_timer(0.1, lambda: self.animate_typing(word, char_idx))
            return

        # Show typing state: "wor_"
        if char_idx <= len(word):
            partial = word[:char_idx]
            self.display_text = format_word_with_orp(partial)
            self.display_text.append("_")
            # 0.031s per character delay from original script
            self.set_timer(
                0.031 / self.wpm_multiplier,
                lambda: self.animate_typing(word, char_idx + 1),
            )
        else:
            # Word complete: "word "
            self.display_text = format_word_with_orp(word)
            self.display_text.append(" ")

            # Calculate wait time based on original logic
            delay = 0.318
            if word and word[-1] in ".:!?":
                delay += 0.360
            elif word and word[-1] in ",;":
                delay += 0.320

            # First word extra delay
            if self.current_index == 0:
                delay = 1.0

            # Schedule next word
            self.current_index += 1
            self.set_timer(delay / self.wpm_multiplier, self.process_step)

    def watch_display_text(self, value: Text) -> None:
        """Update the label when text changes."""
        try:
            self.query_one("#reader-display", Label).update(value)
        except Exception:
            pass

    def watch_current_index(self, value: int) -> None:
        """Update progress bar and display when index changes."""
        try:
            self.query_one(ProgressBar).progress = value
            if self.is_paused and self.words:
                self.display_text = format_word_with_orp(self.words[value])
        except Exception:
            pass

    def watch_wpm_multiplier(self, value: float) -> None:
        """Update speed indicator."""
        try:
            wpm = int(188 * value)
            self.query_one("#speed-indicator", Label).update(
                f"{value:.1f}x ({wpm} wpm)"
            )
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Container(id="display-container"):
            yield Label(self.display_text, id="reader-display")

        with Vertical(id="bottom-section"):
            yield Label("1.0x (188 wpm)", id="speed-indicator")
            yield ProgressBar(total=100, show_eta=False, show_percentage=False)
            yield Footer()

    async def action_quit(self) -> None:
        self.exit()

    def action_toggle_pause(self) -> None:
        if self.current_index >= len(self.words):
            self.current_index = 0
            self.is_paused = False
        else:
            self.is_paused = not self.is_paused

    def action_increase_speed(self) -> None:
        self.wpm_multiplier = min(2.8, self.wpm_multiplier + 0.1)

    def action_decrease_speed(self) -> None:
        self.wpm_multiplier = max(0.1, self.wpm_multiplier - 0.1)

    def action_prev_sentence(self) -> None:
        """Jump to the start of the current or previous sentence."""
        sentence_start = self._find_sentence_start(self.current_index)

        if self.current_index == sentence_start and sentence_start > 0:
            self.current_index = self._find_sentence_start(sentence_start - 1)
        else:
            self.current_index = sentence_start

    def action_next_sentence(self) -> None:
        """Jump to the start of the next sentence."""
        self.current_index = self._find_next_sentence_start(self.current_index)

    def _find_sentence_start(self, from_index: int) -> int:
        """Find the index of the first word of the sentence containing from_index."""
        if from_index <= 0:
            return 0

        for i in range(from_index - 1, -1, -1):
            word = self.words[i]
            if word and word[-1] in ".!?":
                return i + 1
        return 0

    def _find_next_sentence_start(self, from_index: int) -> int:
        """Find the index of the first word of the next sentence after from_index."""
        for i in range(from_index, len(self.words)):
            word = self.words[i]
            if word and word[-1] in ".!?":
                return min(i + 1, len(self.words) - 1)
        return len(self.words) - 1


if __name__ == "__main__":
    main()
