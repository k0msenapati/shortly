# Shortly

Shortly is a simple URL shortener with a clean web interface and a robust API.
It is built with FastAPI, SQLModel, and Jinja2 templates to deliver seamless and responsive link management.

## Use Case

Shortly is designed to simplify link sharing by converting long, complex URLs into concise, readable short codes. It is ideal for sharing links on social media platforms, embedding trackable URLs in print media via QR codes, and managing temporary campaigns with automatic expiration dates.

## Features

- **URL Shortening**: Instantly generate unique short codes (between 7 and 20 characters) for any destination URL.
- **User Accounts**: Register and log in securely to manage, edit, and audit your saved links.
- **Personal Dashboard**: View, search, and manage all your shortened links from a central dashboard.
- **Link Analytics**: Track total clicks and distinguish traffic originating from QR code scans.
- **Expirations**: Set optional expiration dates on links. Expired links automatically return a `410 Gone` status code.
- **Deactivation & Reactivation**: Toggle links on/off or extend their validity dynamically.
- **Advanced Search**: Instantly filter your shortened links by searching long URLs.

## Tech Stack

- **Frontend**: Jinja2 Templates (HTML5/JavaScript), Tailwind CSS
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous ASGI framework)
- **Database**: SQLite (via [SQLModel](https://sqlmodel.tiangolo.com/) and [aiosqlite](https://github.com/omnilib/aiosqlite) for async database support)
- **Auth**: OAuth2 with JWT tokens and Argon2 password hashing (via `pwdlib`)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

## Installation

This project uses `uv` for dependency and environment management.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/k0msenapati/shortly.git
   cd shortly
   ```

2. **Configure environment variables**:
   Create a `.env` file by copying the template:
   ```bash
   cp .env.example .env
   ```
   *Note: Customize the `JWT_SECRET` and database URLs if needed.*

3. **Install dependencies**:
   Sync dependencies and set up the virtual environment:
   ```bash
   uv sync
   ```

## Usage

1. **Start the development server**:
   ```bash
   uv run fastapi dev app/main.py
   ```

2. **Access the application**:
   - Web App UI: Open `http://localhost:8000` in your web browser.
   - Interactive API Docs: Open `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

## Testing

Run the test suite with:

```bash
uv run pytest
```
