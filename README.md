# HarmoniA AI <img src="images/harmonia-logo.png" alt="HarmoniA AI Logo" width="50" align="left">

Inspired by “Harmony” and “AI,” HarmoniA represents a balanced approach to fitness, nutrition, and mental well-being through intelligent conversational agents.


## About HarmoniA

HarmoniA is a multi-agent conversational assistant designed to help users in three key areas of their daily lives:
- Personal Trainer – Provides workout plans, tracks fitness goals, and gives exercise recommendations.
- ️Chef & Nutritionist – Creates personalized recipes, suggests meal plans, and tracks dietary habits.
- Mental Coach – Supports mindfulness, motivation, and overall mental well-being through guided advice.

This AI-powered assistant leverages LangChain, OpenAI, and Chainlit to provide real-time responses tailored to user needs.

## Features

**Conversational AI** – Natural and engaging interactions with specialized agents.
**Multi-Agent System** – Switch between fitness, nutrition, and mental health seamlessly.
**Google Drive Integration** – Upload and retrieve workout plans, meal guides, and mindfulness exercises.
**Memory & Context Retention** – Keeps track of past interactions for a personalized experience.
**Real-Time Processing** – Asynchronous streaming for fast responses.

## Setup & Installation

1. Clone the repository:
    ```
    git clone https://github.com/giorgiocerro/harmonia-ai.git
    cd harmonia
    ```

2. Install dependencies:
    ```
    pip instal -r requirements.txt
    ```

3. Set up environment variables (.env file):
   ```
   OPENAI_API_KEY=your-api-key
   GOOGLE_CREDENTIALS=path-to-google-credentials.json
   ```

4. Run the conversational agent:
   ```
   chainlit run demo.py
   ```

## Usage

Start the chat and type commands like:
- "Give me a 30-minute workout plan." (Personal Trainer)
- "Suggest a high-protein meal." (Chef & Nutrionist)
- "Help me reduce stress today." (Mental Coach)

