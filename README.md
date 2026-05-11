# Micro-Content Recommender

An AI-powered micro-content recommender built with Python and Streamlit. This application suggests quick, context-aware activities based on the user's current energy level, location, time of day, and historical feedback. 

## Features

- **Context-Aware Recommendations**: Uses factors like time of day and energy level to determine the user's "moment type" and suggest relevant activities.
- **Feedback Loop**: Implements Thompson Sampling (Beta distribution) to personalize suggestions over time based on user feedback (thumbs up/down).
- **LLM Fallback**: If no standard activities match the criteria, it gracefully falls back to generating personalized activities dynamically via the Gemini API.

## Project Structure

- `project/app.py`: The main Streamlit web application.
- `activities.py`: The core recommendation engine logic.
- `core/moment_logic.py`: Handles determining the "moment type" from user context.
- `models/feedback_score.py` & `feedback_store.py`: Local SQLite database logic and Thompson Sampling implementation to track activity feedback.
- `services/llm.py` & `gemini_client.py`: Integrates with the Gemini API to provide dynamically generated activities.
- `activities_dataset.json`: A baseline set of general activities.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd micro_content_recommender
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r project/requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

5. **Run the Application:**
   ```bash
   PYTHONPATH=. streamlit run project/app.py
   ```

## Requirements
- Python 3.8+
- Streamlit
- Google Generative AI (`google-generativeai`)
- Numpy
- python-dotenv
