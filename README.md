# MediTranslateAI

MediTranslateAI is an advanced medical translation application designed to accurately translate medical leaflets from Hebrew to English. It leverages state-of-the-art language models and evaluation metrics to ensure high-quality translations of complex medical terminology and information.

## Features

- Translate medical leaflets from Hebrew to English
- Utilize multiple advanced language models for translation
- Evaluate translations using various metrics (BLEU, CHRF, WER)
- Store and manage translation history
- Generate downloadable DOCX files of translations
- User-friendly web interface for easy interaction

## Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local development)
- Python 3.11 (for local development)

## Installation and Setup

1. Set up environment variables:
   - Copy `.example.env` files to `.env.development` and `.env.test`
   - Fill in the required API keys and configuration values

2. Start the development environment:
   ```
   ./dev.ps1
   ```
   This will build and start the Flask backend, React frontend, and MongoDB containers.

3. Access the application at `http://localhost:5173`

## Usage

1. Navigate to the web interface
2. Enter the Hebrew text from a medical leaflet
3. Click "Translate" to get the English translation
4. View, save, or download the translated content

## Project Structure

- `flask_backend/`: Python Flask backend
  - `app.py`: Main Flask application
  - `routes/`: API route definitions
  - `services/`: Core translation and evaluation services
  - `utils/`: Utility functions and helpers
- `react_frontend/`: React frontend application
- `docker-compose.dev.yml`: Docker Compose configuration for development
- `docker-compose.test.yml`: Docker Compose configuration for testing

## Testing

To run the test suite:

```
./test.ps1
```

This will build and run the test environment using Docker.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). This means:

- You are free to use, modify, and distribute this software.
- If you distribute this software or any derivative works, you must do so under the same GPL-3.0 license.
- You must make the source code available when you distribute the software.
- Changes made to the code must be documented.

For more details, see the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).