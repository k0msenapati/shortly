# Shortly

A simple, fast URL shortener with a clean web interface.

## Features

- **URL Shortening**: Instantly create short links for long URLs.
- **User Accounts**: Register and log in to keep track of your links.
- **Personal Dashboard**: Manage all your shortened URLs in one place.
- **Link Analytics**: Track total clicks and identify QR code scans.
- **Expirations**: Secure your links by setting optional expiration dates.
- **Modern Web UI**: Built with Jinja2 templates for a seamless experience.

## Tech Stack

- **Language**: Python 3.13+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic) with SQLite
- **Auth**: JWT (JSON Web Tokens) & Argon2 hashing
- **Frontend**: HTML5, Jinja2 Templates
- **Environment**: [uv](https://github.com/astral-sh/uv) for fast package management

## Installation

This project uses `uv` for dependency management.

1. **Clone the repo**:
   ```bash
   git clone <repo-url>
   cd shortly
   ```

2. **Setup environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `DATABASE_URL` and `JWT_SECRET`.

3. **Install dependencies**:
   ```bash
   uv sync
   ```

## Usage

1. **Start the server**:
   ```bash
   uv run fastapi dev app/main.py
   ```
2. **Access the app**:
   Open `http://localhost:8000` in your browser.


## Testing

Run the test suite with:

```bash
uv run pytest
```
