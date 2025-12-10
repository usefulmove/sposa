from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ProgressBar
from textual.containers import Container
from textual.reactive import reactive
import sys


class SposaApp(App):
    """A Textual app for RSVP reading."""

    TITLE = "Sposa"
    ENABLE_COMMAND_PALETTE = False

    CSS = """
    /* Catppuccin Mocha Theme */
    $base: #1e1e2e;
    $text: #cdd6f4;
    $mauve: #cba6f7;
    $surface0: #313244;
    $overlay0: #6c7086;
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
    
    #status-bar {
        dock: bottom;
        height: 3;
        width: 100%;
        background: $surface0;
        layers: base overlay;
    }

    #speed-indicator {
        layer: overlay;
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $overlay0;
        background: 0%;
        text-align: center;
    }

    ProgressBar {
        layer: base;
        width: 100%;
        height: 100%;
        padding: 0;
    }
    
    Bar {
        width: 100%;
        height: 100%;
        background: $surface0;
    }
    
    Bar > .bar--bar {
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
        ("q", "quit", "Quit"),
        ("space", "toggle_pause", "Play/Pause"),
        ("up", "increase_speed", "Faster"),
        ("down", "decrease_speed", "Slower"),
        ("left", "prev_word", "Back"),
        ("right", "next_word", "Forward"),
        ("h", "prev_word", None),
        ("l", "next_word", None),
        ("k", "increase_speed", None),
        ("j", "decrease_speed", None),
    ]

    # Reactive state
    display_text: reactive[str] = reactive("")
    is_paused: reactive[bool] = reactive(True)
    wpm_multiplier: reactive[float] = reactive(1.0)
    current_index: reactive[int] = reactive(0)

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

        if self.words:
            self.display_text = self.words[0]

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
            self.display_text = f"{word[:char_idx]}_"
            # 0.031s per character delay from original script
            self.set_timer(
                0.031 / self.wpm_multiplier,
                lambda: self.animate_typing(word, char_idx + 1),
            )
        else:
            # Word complete: "word "
            self.display_text = word + " "

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
            pass

    def watch_current_index(self, value: int) -> None:
        """Update progress bar when index changes."""
        try:
            self.query_one(ProgressBar).progress = value
        except Exception:
            pass

    def watch_wpm_multiplier(self, value: float) -> None:
        """Update speed indicator."""
        try:
            wpm = int(188 * value)
            self.query_one("#speed-indicator", Label).update(
                f"{value:.1f}x ({wpm} WPM)"
            )
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="display-container"):
            yield Label(self.display_text, id="reader-display")

        with Container(id="status-bar"):
            yield ProgressBar(total=100, show_eta=False, show_percentage=False)
            yield Label("1.0x (188 WPM)", id="speed-indicator")

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

    def action_prev_word(self) -> None:
        self.current_index = max(0, self.current_index - 10)

    def action_next_word(self) -> None:
        self.current_index = min(len(self.words) - 1, self.current_index + 10)


if __name__ == "__main__":
    app = SposaApp()
    app.run()
