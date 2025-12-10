from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ProgressBar
from textual.containers import Container
from textual.reactive import reactive
import sys
import asyncio


class SposaApp(App):
    """A Textual app for RSVP reading."""

    CSS = """
    /* Catppuccin Mocha Theme */
    $base: #1e1e2e;
    $text: #cdd6f4;
    $mauve: #cba6f7;
    $surface0: #313244;
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
        text-style: bold;
        color: $text;
        height: auto;
    }
    
    ProgressBar {
        dock: bottom;
        margin: 1 2;
        background: $surface0;
        color: $mauve;
    }
    
    Bar > .bar--complete {
        color: $mauve;
    }

    Header {
        background: $surface0;
        color: $mauve;
        dock: top;
    }

    Footer {
        background: $surface0;
        color: $lavender;
        dock: bottom;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("space", "toggle_pause", "Play/Pause"),
        ("up", "increase_speed", "Faster"),
        ("down", "decrease_speed", "Slower"),
        ("left", "prev_word", "Back"),
        ("right", "next_word", "Forward"),
    ]

    # Reactive state
    display_text = reactive("")
    is_paused = reactive(False)
    wpm_multiplier = reactive(1.0)
    current_index = reactive(0)

    # Internal state
    words: list[str] = []

    def on_mount(self) -> None:
        """Load content and start the reader."""
        try:
            filename = sys.argv[1]
            with open(filename, "r") as file:
                self.words = [word.lower() for word in file.read().split()]
        except (IndexError, FileNotFoundError):
            self.words = [
                "sposa",
                "ready",
                "to",
                "read",
                "please",
                "provide",
                "a",
                "file",
            ]

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
            self.display_text = "Done."
            return

        word = self.words[self.current_index]

        # Typing effect logic could go here, but let's implement the base read first
        # to match the mental model of 'Textual' as non-blocking.
        # We'll simulate the "typing" and "waiting" phases.

        self.animate_typing(word)

    def animate_typing(self, word: str, char_idx: int = 1) -> None:
        """Recursive typing effect."""
        if self.is_paused:
            self.set_timer(0.1, lambda: self.animate_typing(word, char_idx))
            return

        # Show typing state: "wor_"
        if char_idx <= len(word):
            self.display_text = f"{word[:char_idx]}_"
            # 0.031s per character delay from original script
            self.set_timer(
                0.031 / self.wpm_multiplier,
                lambda: self.animate_typing(word, char_idx + 1),
            )
        else:
            # Word complete: "word "
            self.display_text = word

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

    def watch_display_text(self, value: str) -> None:
        """Update the label when text changes."""
        try:
            self.query_one("#reader-display", Label).update(value)
        except Exception:
            # Widget might not be mounted yet
            pass

    def watch_current_index(self, value: int) -> None:
        """Update progress bar when index changes."""
        self.query_one(ProgressBar).progress = value

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="display-container"):
            yield Label(self.display_text, id="reader-display")
        yield ProgressBar(total=100, show_eta=True)
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit(self) -> None:
        self.exit()

    def action_toggle_pause(self) -> None:
        self.is_paused = not self.is_paused

    def action_increase_speed(self) -> None:
        self.wpm_multiplier += 0.1
        self.notify(f"Speed: {self.wpm_multiplier:.1f}x")

    def action_decrease_speed(self) -> None:
        self.wpm_multiplier = max(0.1, self.wpm_multiplier - 0.1)
        self.notify(f"Speed: {self.wpm_multiplier:.1f}x")

    def action_prev_word(self) -> None:
        self.current_index = max(0, self.current_index - 10)
        self.notify("Back 10 words")

    def action_next_word(self) -> None:
        self.current_index = min(len(self.words) - 1, self.current_index + 10)
        self.notify("Forward 10 words")


if __name__ == "__main__":
    app = SposaApp()
    app.run()
