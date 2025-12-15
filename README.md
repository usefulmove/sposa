# Sposa

A fast, keyboard-driven RSVP (Rapid Serial Visual Presentation) reader for the terminal.

## Features

- **Speed reading** with Optimal Recognition Point (ORP) highlighting
- **Multiple input sources**: Read from files or clipboard
- **Adjustable speed**: 24-683 WPM (default: 244 WPM)
- **Sentence navigation**: Jump forward/backward by sentence
- **Vim-style keybindings**: hjkl navigation

## Installation

```bash
# Clone and install with uv
git clone <repository-url>
cd sposa
uv sync

# Or install directly (if packaged)
pip install -e .
```

## Usage

### Read from file
```bash
sposa myfile.txt
sposa reads/meditations
```

### Read from clipboard
```bash
# Copy text to clipboard, then:
sposa :clipboard:
# or
sposa --clipboard
```

### Help
```bash
sposa --help
```

## Controls

| Key | Action |
|-----|--------|
| `space` | Play/Pause |
| `↑` / `k` | Increase speed |
| `↓` / `j` | Decrease speed |
| `→` / `l` | Next sentence |
| `←` / `h` | Previous sentence |
| `q` | Quit |

## Speed Range

- **Default**: 244 WPM (1.0x)
- **Minimum**: 24.4 WPM (0.1x)
- **Maximum**: 683.2 WPM (2.8x)
- **Increment**: 0.1x per keypress

## Development

```bash
# Run tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run linter
uv run ruff check .

# Format code
uv run ruff format .

# Type check
uv run ty check .
```

## License

See LICENSE file.
