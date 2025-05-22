# 🌍 AI Travel Planner

## 📋 Features

- **Travel Recommendations**: Get AI-powered suggestions for restaurants, hotels, attractions, activities, and more
- **Local Information**: View current weather, local time, and currency exchange rates
- **Destination Insights**: Access cultural and contextual information about your destination
- **Modern UI**: Dark-themed, responsive interface with smooth animations
- **Multiple AI Models**: Leverages both Google's Gemini and Ollama's models for enhanced recommendations

  ## Documentation :
  https://medium.com/@abhayemani8/ai-travel-planner-technical-documentation-bfa4d08e4985

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Flask
- Access to Google's Gemini API
- Ollama installed locally

### Environment Setup

1. Clone this repository:

bash

```bash
git clone https://github.com/MONARCH1108/Travel_planner.git
cd ai-travel-planner
```

2. Create a virtual environment:

bash

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

bash

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory with the following variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Running the Application

Start the Flask development server:

bash

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## 📊 Project Structure

```
ai-travel-planner/
├── app.py                  # Main Flask application file
├── .env                      # Environment variables (not tracked in git)
├── requirements.txt        # Python dependencies
├── templates/                # HTML templates
│   └── index.html           # Main application template
└── README.md             # This file

```

## 🧩 How It Works

1. **User Input**: The user selects what they're looking for (restaurants, hotels, attractions, etc.) and their destination.
2. **Data Collection**: The application gathers relevant information:
    - Current weather data for the location (via Gemini AI)
    - Local time approximation
    - Currency exchange rates
3. **AI Processing**:
    - Google's Gemini model provides contextual information about the destination
    - Ollama LLM generates personalized recommendations based on the combined data
4. **Presentation**: Results are displayed in an intuitive, visually appealing interface.

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **AI/ML**:
    - Google Generative AI (Gemini-2.0-flash)
    - Ollama (Llama3.2)
- **Frontend**:
    - HTML5/CSS3
    - JavaScript
    - Font Awesome
    - Animate.css
- **APIs**:
    - World Time API
    - Open Exchange Rates API

## 🚦 Version Information

This repository contains two versions of the AI Travel Planner:

- **Version 1**: A Streamlit-based application using Gemini LLM
- **Version 2**: A Flask-based web application using both Gemini and Ollama LLMs

The current README focuses on Version 2 (Flask-based).

## ⚙️ Configuration Options

You can modify the following in the application:

1. **AI Models**: Change the models in use in `app.py`:
    
    python
    
    ```python
    # For Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # For Ollama
    ollama_response = ollama.generate(model="llama3.2", prompt=enriched_prompt)
    ```
    
2. **UI Theme**: Modify the CSS variables in `templates/index.html` to change the color scheme.

## 🔍 API Endpoints

- `GET /`: Main application interface
- `POST /`: Submit travel queries
- `GET /api/weather?location={city}`: Get weather data for a specific location

## 🧪 Future Enhancements

- User authentication and saved trips
- Integration with actual booking services
- Offline capability for travel guides
- Multi-language support
- AI-generated travel itineraries
- Social sharing functionality


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
