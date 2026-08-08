# AI Career Connect

An AI-powered career guidance platform designed to assist users in their professional development journey. Built with Flask and Mistral AI, it offers comprehensive features like resume analysis, interview preparation, career roadmap generation, and a dynamic dashboard.

---

## 🚀 Features

*   **User Registration & Authentication**: Secure sign-up and login system using Flask-Login and Werkzeug password hashing.
*   **AI Chat Assistant**: Interactive chat interface powered by Mistral AI, offering personalized career advice. Supports voice input using the Web Speech API.
*   **Career Roadmap Generator**: Generate customized, step-by-step career transition roadmaps based on your current skills and desired role.
*   **Resume Analyzer**: Get instant AI feedback on your resume, highlighting strengths, weaknesses, and optimization strategies for ATS.
*   **Interview Question Analyzer**: Generate tailored behavioral, technical, and situational interview questions with expected answers for specific job roles.
*   **Dynamic Dashboard**: A visual overview of your activity, including recent conversations and usage statistics with Chart.js.
*   **Speech-to-Text (STT) & Text-to-Speech (TTS)**: Endpoints to handle audio files and text-to-audio conversion using Google APIs.

## 🛠️ Technology Stack

*   **Backend**: Python, Flask (Application Factory Pattern)
*   **Database**: SQLite
*   **ORM**: SQLAlchemy (with Flask-Migrate for migrations)
*   **AI Integration**: Mistral AI API
*   **Frontend**: HTML, CSS, JavaScript
*   **Styling**: Bootstrap 5, Custom CSS with Glassmorphism
*   **Speech Services**: SpeechRecognition, gTTS

## 📁 Project Structure

The application follows the Flask Application Factory pattern, separating concerns into modules:

```text
AI_CARRER_CONNECT/
├── app/
│   ├── models/          # Database models (User, Career, Conversation)
│   ├── routes/          # Flask Blueprints (Endpoints for Auth, Dashboard, Chat, Career, etc.)
│   ├── services/        # Business logic (Mistral AI wrapper, STT/TTS logic, Career logic)
│   ├── static/          # Static assets (CSS, JS, Images, Audio)
│   ├── templates/       # Jinja2 HTML templates
│   ├── utils/           # Helper functions and decorators
│   ├── __init__.py      # App factory initialization
│   └── config.py        # Environment configurations
├── instance/            # Contains the SQLite database file
├── migrations/          # Database migration scripts
├── tests/               # Pytest suite
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── run.py               # Main entry point to start the server
```

## ⚙️ Setup and Installation

### Prerequisites

*   Python 3.10+
*   Mistral AI API Key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI_CARRER_CONNECT
```

### 2. Set up a virtual environment

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create or edit the `.env` file in the root directory. You must provide a valid Mistral API key and a secret key for Flask sessions.

```ini
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///ai_career_connect.db

# Add your Mistral API key here
MISTRAL_API_KEY=your-mistral-api-key-here
```

### 5. Initialize the Database

The application factory (`app/__init__.py`) is set up to automatically create the database tables within the application context on startup.

### 6. Run the Application

```bash
python run.py
```

The server will start on `http://127.0.0.1:5000`.

## 🧪 Running Tests

The project uses `pytest` for automated testing. To run the test suite:

```bash
pytest tests/ -v
```

## 📝 License

This project is open-source and available under the MIT License.
