# 🌤️ Weather ETL Pipeline

An automated data pipeline that collects, transforms and stores real-time weather data from the OpenWeatherMap API.

## 🏗️ Architecture
```
OpenWeatherMap API → Extract → Transform → Load (SQLite) → Streamlit Dashboard
```

## ⚙️ Features

- Automated weather data ingestion every 3 hours
- Data cleaning and transformation with pandas
- Persistent storage in a SQLite database
- Interactive dashboard with Streamlit and Plotly
- Containerized with Docker

## 🛠️ Tech Stack

| Tool | Usage |
|---|---|
| Python | Core language |
| Requests | REST API calls |
| Pandas | Data transformation |
| SQLAlchemy | ORM and database connection |
| SQLite | Data storage |
| Schedule | Pipeline automation |
| Streamlit | Visualization dashboard |
| Plotly | Interactive charts |
| Docker | Containerization |
| Railway | Cloud deployment |

## 📊 Dashboard

The dashboard displays for each city :
- Average, min and max temperature over 5 days
- Humidity evolution
- Wind speed

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker
- OpenWeatherMap account (free API key)

### Run locally

1. Clone the repo
```bash
git clone https://github.com/your-username/Weather-ETL-Pipeline.git
cd Weather-ETL-Pipeline
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file
```
API_KEY=your_openweathermap_key
```

4. Run the pipeline
```bash
python main.py
```

5. Run the dashboard
```bash
streamlit run dashboard.py
```

### Run with Docker
```bash
docker build -t weather-pipeline .
docker run --env-file .env weather-pipeline
```

## 📁 Project Structure
```
Weather-ETL-Pipeline/
├── extract.py        # API call and pandas structuring
├── load.py           # SQLite storage
├── main.py           # Orchestration and scheduler
├── dashboard.py      # Streamlit dashboard
├── Dockerfile        
├── requirements.txt  
├── .env              # Environment variables (not committed)
├── .gitignore        
└── .dockerignore     
```

## 🔄 ETL Pipeline

**Extract** — Calls the OpenWeatherMap `forecast` endpoint to retrieve 5-day weather forecasts (40 entries per city, every 3 hours).

**Transform** — Data cleaning with pandas: Kelvin → Celsius conversion, selection of relevant fields (temperature, humidity, wind speed), structuring into a DataFrame.

**Load** — Storage in a SQLite database via SQLAlchemy with history management.

