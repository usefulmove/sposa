# Textual Migration Plan for Sposa

## 1. Objective
Migrate the existing `sposa` RSVP (Rapid Serial Visual Presentation) prototyping tool from a synchronous, `sleep`-based CLI script to a robust, event-driven TUI application using the **Textual** framework.

## 2. Rationale
The current implementation uses blocking `time.sleep` calls, which makes implementing interactivity (pause, rewind, speed adjustment) difficult. Textual provides a non-blocking event loop, native keyboard handling, and reactive state management, enabling a responsive and rich user experience while maintaining the precise timing required for RSVP reading.

## 3. Core Architecture

### 3.1. The "Tick" Engine
Instead of a blocking loop, we will use a recursive timer pattern.
*   **Old Way:** `print(word); sleep(delay);`
*   **New Way:** `display(word); set_timer(delay, next_step)`
This allows the UI to remain responsive (e.g., to pause commands) during the "wait" periods between words.

### 3.2. State Management (Reactive)
We will utilize Textual's `reactive` attributes to automatically trigger UI updates.
*   `current_word`: The word currently being displayed.
*   `wpm_multiplier`: A float to adjust reading speed dynamically.
*   `is_paused`: Boolean state to halt the recursive timer.
*   `progress_index`: Integer tracking position in the word list.

## 4. Implementation Phases

### Phase 1: Dependencies & Scaffolding
1.  **Add Dependency:** Add `textual` to `pyproject.toml` (or `requirements.txt`).
2.  **Create File:** Initialize `sposa_tui.py`.
3.  **Basic App:** Create a subclass of `App` with a placeholder `Label` and `Footer`.

### Phase 2: Logic Porting
1.  **Word Loader:** Adapt the existing file reading and word tokenization logic.
2.  **Delay Calculation:** Extract the delay logic (0.318s base, punctuation scaling) into a pure function `calculate_delay(word, wpm_multiplier)`.
3.  **Engine Implementation:** Implement the `step()` method that orchestrates the word updates and timer scheduling.

### Phase 3: UI Components
1.  **Display Widget:** Create a customized `Label` or `Static` widget for the main text, styled with CSS for large, centered text.
2.  **Progress Bar:** Integrate `textual.widgets.ProgressBar` to show reading progress.
3.  **Footer:** Configure the `Footer` widget to show available keybindings.

### Phase 4: Interactivity & Controls
1.  **Pause/Play:** `SPACE` key toggles `is_paused`.
2.  **Speed Control:** `UP`/`DOWN` arrows modify `wpm_multiplier`.
3.  **Navigation:** `LEFT`/`RIGHT` arrows jump +/- 10 words (or to start/end of sentences).
4.  **Quit:** `Q` or `ESC` to exit.

## 5. Proposed File Structure (`sposa_tui.py`)

```python
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Label, ProgressBar

class SposaApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #reader-display {
        text-align: center;
        height: 1fr;
        content-align: center middle;
        text-style: bold;
        color: white;
    }
    """

    BINDINGS = [
        ("space", "toggle_pause", "Play/Pause"),
        ("up", "increase_speed", "Faster"),
        ("down", "decrease_speed", "Slower"),
        ("q", "quit", "Quit"),
    ]

    # ... implementation details ...
```

## 6. Next Steps
1.  Execute **Phase 1** to set up the environment.
2.  Begin **Phase 2** to get the text moving on screen.
