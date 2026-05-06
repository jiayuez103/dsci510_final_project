# Analyzing Winter Airbnb Pricing Drivers Using Weather and Google Trends in Skaneateles Lake, NY <Project title> 

This project analyzes factors that influence winter Airbnb pricing in Skaneateles Lake and Canandaigua Lake, NY. Using Airbnb listing data via API, historical weather data, and Google Trends time series data, I examine how weather conditions, local events, and seasonal trends affect nightly winter prices across two Finger Lakes regions over two winter seasons (2023–2025). I build Random Forest models to identify key pricing drivers and validate findings across regions.


# Data sources
| # | Name               | Source URL                   | Type        | Key Fields                                                                     | Format | Size                                                                                  |
|---|--------------------|------------------------------|-------------|--------------------------------------------------------------------------------|--------|---------------------------------------------------------------------------------------|
| 1 | Airbnb Listings    | RapidAPI Airbnb Listings API | API         | listing_id, date, price_usd, bedrooms, star_rating, review_count, is_superhost | JSON   | Skaneateles: 136 listings, 25,131 records / Canandaigua: 285 listings, 53,565 records |
| 2 | Historical Weather | Rapid API Meteostat API      | API         | date, tavg, tmin, tmax, snow, prcp                                             | JSON   | Each region: 454 records                                                              |
| 3 | Search Trends      | Google Trends (pytrends)     | API wrapper | date, keyword, interest (0-100)                                                | CSV    | Skaneateles; 1,362 / Canandaigua: 2,270                                               |

After merging all three data sources:
- Skaneateles: 19,360 data points 
- Canandaigua: 42,137 data points

# Analysis
This project uses a per-listing Random Forest Regressor to identify key pricing drivers for winter Airbnb listings. For each listing, features include weather conditions (average temperature, snowfall), calendar features (month, year, weekend), and Google Trends search interest for region-specific keywords. A second full model is trained on all listings combined using normalized prices (price divided by listing average) to identify overall market-wide drivers. Results are compared across two Finger Lakes regions to test whether findings generalize.

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
- Prices increased approximately 48% from 2023-2024 ($300) to 2024-2025 ($450) in Skaneateles, confirming year as a strong pricing signal

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

Required packages include: `requests`, `pandas`, `pytrends`, `python-dotenv`, `scikit-learn`, `matplotlib`, `seaborn`, `numpy`, `joblib`

# Running analysis

All commands should be run from the `src/` directory:
```
cd src
```

**Step 1: Train models**

As loading all the listing data from Airbnb API used in this project requires 5,000+ API calls and take several hours to finish, pre-collected and merged datasets are provided through Google Drive. 

Both links must be provided together to train the model.

```bash
python main.py --train \
  --data_link_skaneateles "https://drive.google.com/uc?export=download&id=1TE1x4qej5NB_fblGA7HOQzFn6Ck1Lnsz" \
  --data_link_canandaigua "https://drive.google.com/uc?export=download&id=1P3b8GlopCmrJRfNhSt9BEyBR19hFeRs_"
```

Alterative：If training from original data sources, it requires Rapid API account and RAPIDAPI_KEY.
```bash
python main.py --train
```
It will:
1. Collect weather data from Meteostat API for both regions
2. Collect Google Trends data for region-specific keywords
3. Collect Airbnb listing prices via RapidAPI
4. Merge all three data sources
5. Train Random Forest models per listing
6. Train full normalized model
7. Save trained models to `results/`

**Step 2：Evaluate Models**
**Skaneateles:**
```bash
python main.py --evaluation --model_link "https://drive.google.com/uc?export=download&id=1N1Z9ZE0okHkXIQDlBl6dqtb7m8DuhjWC" --region skaneateles
```

**Canandaigua:**
```bash
python main.py --evaluation --model_link "https://drive.google.com/uc?export=download&id=1f_vjSXTVGgU_M5EggCfx4QqILFcFpCjB" --region canandaigua
```

## Download Pre-collected Data Link (Google Drive)
- Skaneateles Lake merged data: https://drive.google.com/uc?export=download&id=1TE1x4qej5NB_fblGA7HOQzFn6Ck1Lnsz
- Canandaigua Lake merged data: <https://drive.google.com/uc?export=download&id=1P3b8GlopCmrJRfNhSt9BEyBR19hFeRs_>
## Download Pre-trained Model Link (Google Drive)
- Skaneateles model: https://drive.google.com/uc?export=download&id=1N1Z9ZE0okHkXIQDlBl6dqtb7m8DuhjWC
- Canandaigua model: https://drive.google.com/uc?export=download&id=1f_vjSXTVGgU_M5EggCfx4QqILFcFpCjB

Results will appear in `results/` folder. All data will be stored in `data/`.

## AI Assistance

This project used Claude to solve some difficult challenges, as stated below:
- In `load.py`: use AI to generate `timeout=20` parameter in API requests. This is added after whole program froze when collecting listing data via API, causing the program to hang indefinitely without any error message
- In `load.py`: use AI to generate `time.sleep()` after getting blocked a few times due to frequent API calls
- In `main.py`: use AI to help with model download logic using `urllib.request` in the `evaluate()` function 

All AI-generated code sections have been labeled with `# AI generated` comments.