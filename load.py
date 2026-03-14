from sqlalchemy import create_engine

def load_to_db(df):
    engine = create_engine("sqlite:///meteo.db")
    return df.to_sql(name="meteo",con=engine,if_exists="append")