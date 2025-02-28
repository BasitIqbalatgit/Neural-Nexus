# Multimodal AI Assistant

A versatile AI assistant that combines text, voice, and file input capabilities with Gemini AI and weather information integration.

## Features

- Multiple input modes (text, voice, file upload)
- Integration with Google's Gemini AI
- Real-time weather information
- Conversation history management
- File analysis support (images, PDFs, documents)
- Voice input processing

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- OpenWeatherMap API key (get it from [OpenWeatherMap](https://openweathermap.org/api))

## Security Notice

This project uses environment variables for API keys. Never commit your actual `.env` file to GitHub.

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd AI-HACK
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.sample .env
```
Then edit `.env` with your actual API keys.

## Configuration

The `.env` file should contain:
```plaintext
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

## Project Structure

```
AI-HACK/
├── .env.sample           # Template for environment variables
├── .gitignore           # Git ignore rules
├── config.py            # Configuration and API keys
├── utils/
│   ├── __init__.py
│   ├── api_handler.py   # API interaction handlers
│   └── context_manager.py # Conversation context management
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

3. Choose your preferred input mode:
   - Text: Type your message
   - Voice: Use microphone input
   - Upload: Share files for analysis

4. For weather information, include "weather" in your query:
   Example: "What's the weather in London?"

## Error Handling

The application includes comprehensive error handling for:
- API failures
- File upload issues
- Voice recognition errors
- Missing API keys

## Logging

All operations are logged to `app.log` with timestamps and error details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
