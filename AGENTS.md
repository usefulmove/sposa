# AGENTS.md - Development Guidelines

## Project Overview
Sposa is an RSVP (Rapid Serial Visual Presentation) reader application built with Python and [Textual](https://textual.textualize.io/).
It has migrated from a raw `sys.stdout` prototype to a robust, event-driven TUI application.

## Running the Application
- Run the TUI: `uv run python sposa_tui.py <filename>`
- Example: `uv run python sposa_tui.py meditations`
- Dependency Management: Uses `uv` for package management.

## Build/Lint/Test Commands
- Run tests: `python -m pytest`
- Linting: `ruff check .`
- Formatting: `ruff format .`
- Type checking: `ty check .`

## Code Style Guidelines
- Use Python 3.13+ syntax.
- Follow PEP 8.
- Use type hints for all function parameters and return values.
- **Textual Guidelines**:
    - Use `CSS` class attributes or `.tcss` files for styling.
    - Use `reactive` attributes for state that drives the UI.
    - Avoid blocking calls like `time.sleep()`; use `self.set_timer()` or `self.set_interval()`.
    - Use specific `Action` methods (e.g., `action_quit`) for keybindings.

## Import Guidelines
- Use standard library imports first, then third-party (like `textual`), then local imports.
- Group imports at the top of each file.
- Use explicit imports (avoid `from module import *`).

## Error Handling
- Use specific exception handling rather than broad except clauses.
- Handle file I/O errors gracefully (e.g., when loading the text file).

## Testing
- Write unit tests for logic where possible.
- TUI interaction tests can be complex; prioritize testing the underlying logic (e.g., text splitting, delay calculations).
- Run a single test with: `python -m pytest -xvs tests/test_specific.py::test_function`

## Code Quality
- Keep functions small and focused.
- Run linters (`ruff`) before committing.
- Format code (`ruff format`) before pushing.
