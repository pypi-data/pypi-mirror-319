# slimcontext

**slimcontext** is a Python package that transforms a Git repository into contextual information suitable for Large Language Models (LLMs). It extracts comprehensive information from Python source files, generates structured context for LLMs, and provides utilities for token counting and logging.

## Features

- **Context Extraction:** Extracts either full or slim textual contexts based on the repository content, tailored for effective LLM interactions.
- **Token Counting:** Integrates with `tiktoken` to count tokens, ensuring compatibility with various LLM models.
- **Command-Line Interface (CLI):** User-friendly CLI built with `Click` for easy interaction and automation.
- **Git Integration:** Manages and interacts with Git repositories, handling file extraction and repository structure efficiently.

## Installation

You can install the package via PyPI:

```bash
pip install slimcontext
```

Or install directly from GitLab:

```bash
pip install git+https://gitlab.com/notorious-community/slimcontext.git
```

## Usage

### Command-Line Interface (CLI)

The package provides a CLI tool for easy interaction. Below are the available commands and options.

#### Basic Usage

```bash
slimcontext main --path /path/to/your/git/repo
```

#### Options

- `--path`: Path to the Git repository (required).
- `--context-level`: Level of context generation (`full` or `slim`). Defaults to `slim`.
- `--output`: Path to the output file. If not specified, outputs to stdout.
- `--token-model`: Specify the model for token counting (e.g., `gpt-4`). Set to `None` to skip token counting.
- `--verbose`: Logging level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Defaults to `WARNING`.

#### Examples

```bash
slimcontext main \
    --path /path/to/your/git/repo \
    --context-level full \
    --output /path/to/output/context.txt \
    --token-model gpt-4 \
    --verbose 0
```

or

```bash
slimcontext main \
    -p /path/to/your/git/repo \
    -c full \
    -o /path/to/output/context.txt \
    -t gpt-4 \
    -v
```

### Python API

```python
from slimcontext import (
    ProjectParser,
    initialize_git_repo,
    generate_context,
    count_tokens,
    write_output,
    setup_logger
)
from pathlib import Path

# Initialize logger
logger = setup_logger(__name__)

# Initialize Git repository
repo_path = Path('/path/to/your/git/repo')
git_repo = initialize_git_repo(repo_dir=repo_path)
files = git_repo.get_abolute_file_paths()

# Initialize Python parser
parser = ProjectParser(root_dir=git_repo.get_git_root())

# Generate context
context = generate_context(parser=parser, files=files, context_level='slim')

# Count tokens
token_count = count_tokens(context=context)
print(f"Total tokens: {token_count}")

# Write output
output_path = Path('/path/to/output/context.txt')
write_output(context=context, output_path=output_path)
```

## Development

### Setting Up the Development Environment

1. **Clone the Repository:**

    ```bash
    git clone https://gitlab.com/notorious-community/slimcontext.git
    cd slimcontext
    ```

2. **Install Dependencies:**

    Ensure you have `poetry` installed. Then run:

    ```bash
    poetry install
    ```

### Running Tests

The package includes a comprehensive test suite using `pytest`.

```bash
poetry run pytest
```

### Linting and Formatting

Ensure code quality and consistency with `ruff`.

```bash
poetry run ruff check .
```

### Running Nox Sessions

Automate development tasks across multiple Python environments using `nox`.

```bash
nox -s tests
```

## Project Structure

```
slimcontext/
├── slimcontext/
│   ├── main.py
│   ├── managers/  # Houses various managers for languages.
│   ├── parsers/  # Houses the code to parse and extract key context by language.
│   └── utils/  # Various utilities used across code base.
├── tests/ 
├── gitlab-ci.yml
├── CHANGELOG
├── LICENSE
├── noxfile.py
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Whether it's reporting bugs, suggesting features, or submitting pull requests, your help is appreciated. Please follow these steps to contribute:

1. **Fork the Repository:**

    Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork:**

    ```bash
    git clone https://gitlab.com/your-username/slimcontext.git
    cd slimcontext
    ```

3. **Create a New Branch:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes:**

    Implement your feature or bug fix.

5. **Commit Your Changes:**

    ```bash
    git commit -m "Title of your changes" -m "Describe **Why** you made this change."
    ```

6. **Push to Your Fork:**

    ```bash
    git push origin feature/your-feature-name
    ```

7. **Create a Merge Request:**

    Go to the original repository and create a merge request from your fork.

Please ensure all tests pass and adhere to the project's coding standards before submitting your merge request.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

**Copyright (c) 2024 Neil Schneider**