from extract import extract_meteo_features
from load import load_to_db
import schedule
import time
cities=["Rome","Paris"]

def run_pipeline(city):
    print(f"Pipeline lancé pour {city}...")
    df=extract_meteo_features(city)
    return load_to_db(df)
for city in cities:
    run_pipeline(city)
    schedule.every(3).hours.do(lambda c=city: run_pipeline(c))

while True:
    schedule.run_pending()
    time.sleep(1)