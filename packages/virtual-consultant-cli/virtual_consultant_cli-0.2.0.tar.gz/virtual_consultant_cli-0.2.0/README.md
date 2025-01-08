# Virtual Consultant CLI

A professional command-line interface tool for creating and managing Virtual Consultant projects.

[![CI](https://github.com/yourusername/virtual-consultant-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/virtual-consultant-cli/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/virtual-consultant-cli.svg)](https://badge.fury.io/py/virtual-consultant-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

## Features

- 🚀 Quick project scaffolding
- 📦 Automated dependency management
- 📝 Documentation generation
- 🔧 Development environment setup
- 🧪 Testing infrastructure
- 🔄 CI/CD configuration

## Installation

```bash
pip install virtual-consultant-cli
```

Or with Poetry:

```bash
poetry add virtual-consultant-cli
```

## Usage

Create a new project:

```bash
vconsult create my-project
```

Set up an existing project:

```bash
cd my-project
vconsult setup
```

Check system dependencies:

```bash
vconsult doctor
```

## Development

Clone the repository:

```bash
git clone https://github.com/yourusername/virtual-consultant-cli.git
cd virtual-consultant-cli
```

Install dependencies:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

Run type checking:

```bash
poetry run mypy virtual_consultant_cli
```

Run linting:

```bash
poetry run ruff check .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install pre-commit hooks (`poetry run pre-commit install`)
4. Make your changes
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
