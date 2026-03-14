import requests
from dotenv import load_dotenv
import os
import pandas as pd


def extract_meteo_features(city):
    load_dotenv()
    api_key=os.getenv('API_KEY')
    URL=f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"


    response = requests.get(URL)
    output=response.json()
    print(output)

    prevision_list=output["list"]

    meteo_features=[]

    for prevision in prevision_list:
        dictionnary_meteo= {
            "datetime": prevision['dt_txt'],
            "city": output['city']['name'] ,
            "temp": prevision['main']['temp']-273.15,
            "temp_min": prevision['main']['temp_min']-273.15,
            "temp_max": prevision['main']['temp_max']-273.15,
            "humidity": prevision['main']['humidity'],
            "windspeed": prevision['wind']['speed']
        }
        meteo_features.append(dictionnary_meteo)
    df=pd.DataFrame(meteo_features)
    return df