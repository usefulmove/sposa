# AGENTS.md - Development Guidelines

## Build/Lint/Test Commands
- Run tests: `python -m pytest` (if pytest is used)
- Linting: `ruff check .` (if using ruff)
- Formatting: `ruff format .`
- Type checking: `ty check .`

## Code Style Guidelines
- Use Python 3.13+ syntax when possible
- Follow PEP 8 for general style guide
- Use type hints for all function parameters and return values
- Use descriptive variable names in snake_case
- Keep functions small and focused
- Use docstrings for all public functions and classes

## Import Guidelines
- Use standard library imports first, then third-party, then local imports
- Group imports at the top of each file
- Use explicit imports (avoid `from module import *`)

## Error Handling
- Use specific exception handling rather than broad except clauses
- Always include meaningful error messages
- Handle errors at appropriate levels in the code

## Testing
- Write unit tests for all new functionality
- Use pytest as the testing framework
- Place test files in a `tests` directory
- Run a single test with: `python -m pytest -xvs tests/test_specific.py::test_function`

## Code Quality
- Keep functions under 50 lines when possible
- Maintain 100% test coverage for new features
- Run linters before committing
- Format code before pushing
