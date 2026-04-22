# Analyzing Winter Airbnb Pricing Drivers Using Weather and Google Trends in Skaneateles Lake, NY <Project title> 
This project analyzes factors that influence winter Airbnb pricing in Skaneateles Lake and Canandaigua Lake, NY. Using Airbnb listing data via API, historical weather data, and Google Trends time series data, I examine how weather conditions, local events, and seasonal trends affect nightly winter prices across two Finger Lakes regions over two winter seasons (2023–2025). I build Random Forest models to identify key pricing drivers and validate findings across regions.


# Data sources
| # | Name               | Source URL                   | Type        | Key Fields                                                                     | Format | Size                                                                                  |
|---|--------------------|------------------------------|-------------|--------------------------------------------------------------------------------|--------|---------------------------------------------------------------------------------------|
| 1 | Airbnb Listings    | RapidAPI Airbnb Listings API | API         | listing_id, date, price_usd, bedrooms, star_rating, review_count, is_superhost | JSON   | Skaneateles: 136 listings, 25,131 records / Canandaigua: 285 listings, 53,565 records |
| 2 | Historical Weather | Rapid API Meteostat API      | API         | date, tavg, tmin, tmax, snow, prcp                                             | JSON   | 1 record/day × 2 regions × 2 seasons = 302 records                                    |
| 3 | Search Trends      | Google Trends (pytrends)     | API wrapper | date, keyword, interest (0-100)                                                | CSV    | 1 record/keyword/day × 2 seasons = 453 records per region                             |

# Results

## Model Performance
Random Forest Regressor was trained per-listing on two winter seasons (2023–2025).

| Region           | Mean R² | Median R² |
|------------------|---------|-----------|
| Skaneateles Lake | 0.546   | 0.610     |
| Canandaigua Lake | 0.436   | 0.473     |

Skaneateles Mean R² > 0.5, indicating the model successfully captures pricing patterns for the primary region. Large variance in per-listing R² (0.0–0.98) reveals two host strategies: dynamic pricing vs. fixed pricing.

## Key Pricing Drivers

**Skaneateles Lake:** month (~38%), year (~17%), trend_syracuse_basketball (~11%), tavg (~11%), trend_dickens_christmas (~10%)

**Canandaigua Lake:** year (~50%), trend_bristol_mountain (~13%), tavg (~11%), trend_finger_lakes (~10%)

Skaneateles pricing is driven by seasonality (month as top feature), while Canandaigua pricing is dominated by year-over-year market changes.

## Pricing Patterns
- Skaneateles average nightly prices are consistently ~$130–$140 higher than Canandaigua across all months
- Skaneateles November and December are the most expensive months (~$420–$422)
- Canandaigua prices are nearly flat across all five months (~$278–$290)
- Prices increased ~48% from 2023–2024 (~$300) to 2024–2025 (~$450) in Skaneateles, confirming year as a strong pricing signal

## Feature Analysis
Temperature, Dickens Christmas trend, and Syracuse Basketball trend show no clear linear effect on price when examined individually. Their importance in the model reflects interaction effects with month and year, not direct causal relationships.

# Installation
## API Keys
This project requires one API key:
- Airbnb Listings + Meteostat API (via RapidAPI) — sign up at rapidapi.com, subscribe to both APIs, and copy your API key.

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

**Train models (collects data + trains + saves models):**

```bash
python main.py --train
```

**Evaluate using pre-trained model (Skaneateles):**
```bash
python main.py --evaluation --model_link https://drive.google.com/file/d/1N1Z9ZE0okHkXIQDlBl6dqtb7m8DuhjWC/view?usp=drive_link --region skaneateles
```

**Evaluate using pre-trained model (Canandaigua):**
```bash
python main.py --evaluation --model_link https://drive.google.com/file/d/1f_vjSXTVGgU_M5EggCfx4QqILFcFpCjB/view?usp=drive_link --region canandaigua
```

## Pre-trained Model Files (Google Drive)
- Skaneateles model: https://drive.google.com/file/d/1N1Z9ZE0okHkXIQDlBl6dqtb7m8DuhjWC/view?usp=drive_link
- Canandaigua model: https://drive.google.com/file/d/1f_vjSXTVGgU_M5EggCfx4QqILFcFpCjB/view?usp=drive_link

Results will appear in `results/` folder. All data will be stored in `data/`.