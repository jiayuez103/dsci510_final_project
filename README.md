# Analyzing Winter Airbnb Pricing Drivers Using Weather and Google Trends in Skaneateles Lake, NY <Project title> 
This project analyzes factors that influence winter Airbnb pricing in Skaneateles Lake, NY. Using scraped Airbnb listing and calendar data, weather API data, and time series data via Google Trends, I will examine how property characteristics, snowfall, and  trend features affect nightly winter prices. I will build regression and random forest models to identify key pricing drivers and compare their predictive performance. The goal is to understand how external demand factors and listing features influence winter pricing behavior. The project integrates web scraping, API data collection, and basic machine learning techniques suitable for an introductory data science course.


# Data sources
| # | Name                        | Source URL                           | Type           | Fields                                                                              | Format | Estimated Data Size                     |
|---|-----------------------------|--------------------------------------|----------------|-------------------------------------------------------------------------------------|--------|-----------------------------------------|
| 1 | Airbnb winter listings      | airbnb.com                           | Web scraping   | listing_id, nightly_price, bedrooms, bathrooms, rating, review_count, property_type | JSON   | Up to 600 properties per search date    |
| 2 | Historical winter weather   | rapidapi.com/meteostat/api/meteostat | API (RapidAPI) | date, tavg, tmin, tmax, prcp, snow                                                  | JSON   | 150 days x 3 winters = 450+ data points |
| 3 | Search interest time series | trends.google.com (pytrends)         | API wrapper    | date, keyword, interest (0-100)                                                     | CSV    | 5 keywords x 3 winters = 600+ records   |

# Results 
_describe your findings_

# Installation
## API Keys
This project requires one API key:
- **Meteostat API** (via RapidAPI) — sign up at rapidapi.com/meteostat/api/meteostat, subscribe to the free plan, and copy your API key.

Create a `.env` file inside the `src/` folder and add:
```
RAPIDAPI_KEY=your_key_here
```

Google Trends (pytrends) does not require an API key.

## Python Packages
Install all required packages:
```
pip install -r requirements.txt
```

Required packages include: `requests`, `pandas`, `pytrends`, `python-dotenv`, `beautifulsoup4`

# Running analysis 
_update these instructions_

From `src/` directory run:

`python main.py `

Results will appear in `results/` folder. All obtained will be stored in `data/`