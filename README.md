
# **Weather Forecast Application**

A Streamlit-powered web application that provides **12-hour weather forecasts** using ensemble models. Users can select a city and country, customize the ensemble technique, and view accurate, real-time predictions generated from multiple public APIs.

## **Features**
- 🌍 **City-Based Forecasting**: Enter a city and country to fetch forecasts for your desired location.
- 📊 **Ensemble Models**: Choose from a variety of ensemble techniques to refine predictions.
- 📡 **API Integration**: Combines data from multiple public weather APIs.
- 🔄 **Real-Time Updates**: Fetches live weather data on user input.
- 📈 **Interactive Visualizations**: Displays temperature, precipitation, wind speed, and other forecast details.

---

## **Getting Started**

### **Prerequisites**
Ensure you have the following installed:
- Python 3.8 or later
- Pip (Python package manager)

### **Installation**
1. Clone this repository:
   ```bash
   git clone [<your-repo-url>](https://github.com/sarmaos/refined_weather_forecasting)
   cd refined_weather_forecasting
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

---

## **Running the Application**
To start the app, navigate to the project directory and run the following command:
```bash
streamlit run app.py
```

This will launch the application in your default web browser.

---

## **Application Structure**

```plaintext
├── api/                  # Contains code for API calls and data fetching
│   ├── api_client.py      # Classes for interacting with weather APIs
│   └── data_fetcher.py    # Utility functions to fetch and clean data
├── model/                # Contains ensemble techniques and ML models
│   ├── ensemble_models.py # Code for weighted averages, linear regression, etc.
│   └── ml_models.py       # Additional ML-based models
├── app.py                # The main entry point for the Streamlit app
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

---

## **How It Works**
1. **Input**: Users select a city and country.
2. **Backend**:
   - The `api` folder handles fetching weather data via API calls and formats the data into **Pandas DataFrames**.
   - The `model` folder contains all the ensemble techniques and machine learning models to process the forecasts.
3. **Output**: The app displays predictions and visualizations in real time based on the selected ensemble technique.

---

## **APIs Used**
This application uses multiple public weather APIs. You will need to configure the appropriate API keys to enable the app to fetch data.

1. Update your API keys in the appropriate configuration file (`api/api_client.py` or similar).
2. Ensure you have access to the APIs used (e.g., OpenWeatherMap, WeatherStack, etc.).

---

## **Example Usage**
1. Launch the app with `streamlit run app.py`.
2. Enter the desired **city** and **country**.
3. Select an ensemble technique (e.g., simple average, weighted average, linear regression).
4. View the 12-hour forecast and analysis generated in real time.

---

## **Screenshots**
*(Optional: Add screenshots or GIFs showcasing your app UI.)*

---

## **Contributing**
If you’d like to contribute to this project, feel free to fork the repository and submit a pull request. Suggestions and improvements are always welcome!

---

## **License**
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

## **Contact**
For support or collaboration, please contact:
- **Spyros Armaos**
- Email: [YourEmail@example.com]
