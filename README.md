```markdown
# Expense Bot

**Expense Bot** is a Telegram bot built with Python to track and analyze your expenses via text and voice input.  
It uses SQLite for data storage, pydub and speech_recognition for audio processing, and includes smart reminders and gamification features to help you manage your budget effectively.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Expense Tracking**: Log your expenses using simple text commands (e.g., "10000 сум на еду") or voice messages.
- **Voice Processing**: Uses [pydub](https://github.com/jiaaro/pydub) and [SpeechRecognition](https://github.com/Uberi/speech_recognition) to convert voice messages into text.
- **Smart Reminders**: Automatically reminds you of upcoming bills and alerts if you haven’t logged expenses for a while.
- **Analytics & Reports**: Provides monthly expense summaries and category breakdowns.
- **Rule-Based Advisor**: Analyzes spending habits and offers tailored advice (e.g., reducing fast food expenses).
- **Gamification**: Rewards users with achievements for consistent tracking or reducing expenses.
- **Database**: Uses SQLite for simple local storage.

## Project Structure

```
expense_bot/
├── bot.py           # Main bot logic and command handlers
├── bot_instance.py  # Creates and exports the bot instance to avoid cyclic imports
├── config.py        # Configuration settings (bot token, reminder intervals, etc.)
├── database.py      # SQLite database setup and functions (expenses, bills, achievements)
├── speech.py        # Voice processing: converting OGG to WAV using pydub and recognizing speech
├── analysis.py      # Basic analytics for expenses (totals, category stats)
├── advisor.py       # Rule-based financial advice based on user spending
├── gamification.py  # Achievement logic and gamification features
├── reminders.py     # Scheduler (apscheduler) for bills, inactivity, and achievements
├── requirements.txt # Python dependencies
└── data/            # Temporary storage for audio files (voice.ogg, voice.wav)
```

## Prerequisites

- **Python 3.8+**  
- **ffmpeg** installed and in your system PATH  
  - On Windows, you can download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via [chocolatey](https://chocolatey.org/):
    ```bash
    choco install ffmpeg
    ```
- **pip** (Python package manager)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourUserName/expense_bot.git
   cd expense_bot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Update the Bot Token** in `config.py`:
   ```python
   # config.py
   TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   BILL_REMINDER_DAYS = 3
   INACTIVITY_DAYS = 2
   ```

2. **Optional Settings**:  
   Adjust any other settings (e.g., reminder intervals, inactivity thresholds).

## Usage

1. **Run the Bot**:
   ```bash
   python bot.py
   ```
2. **Interact on Telegram**:
   - **/start** – Start the bot and get usage instructions.
   - **Text Input** – Send a message like `10000 сум на еду` to log an expense.
   - **Voice Input** – Send a voice message; the bot converts it to text and logs the expense.
   - **/add_bill** – Add a scheduled payment (e.g., `50000 сум, коммунальные, 2025-03-01, monthly`).
   - **/stats** – Get monthly expense stats and category breakdown.
   - **/advice** – Get rule-based financial advice.
   - **/achievements** – See your earned achievements.

## Deployment

### Deploy on a VPS
- Install Python, ffmpeg, and git on your server.
- Clone the repository, create a virtual environment, install dependencies.
- Run `python bot.py`.
- (Optional) Use systemd or Supervisor for automatic restarts.

### Docker Deployment
1. Create a Dockerfile:
   ```dockerfile
   FROM python:3.10-slim
   RUN apt-get update && apt-get install -y ffmpeg
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   ENV TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   CMD ["python", "bot.py"]
   ```
2. Build and run:
   ```bash
   docker build -t expense-bot .
   docker run -d --name expense-bot expense-bot
   ```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements or new features.

```

