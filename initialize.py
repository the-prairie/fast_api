import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os

from database import SessionLocal, engine
import models

from pydantic import BaseModel


load_dotenv()



def get_coins():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ.get("COINMARKETCAP_KEY"),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return pd.json_normalize(data['data'])


def get_coin_meta(coins):
    
    coin_list = []

    for i in range(0, len(coins), 100):
        slice_item = slice(i, i+100, 1)
        coin_list.append(','.join([str(x) for x in coins[slice_item]]))

    
    
    coin_meta = []
    
    for i in range(len(coin_list)):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        parameters = {
            'id': coin_list[i]
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get("COINMARKETCAP_KEY"),
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        if data.get('data'):
            coin_meta.append(pd.json_normalize(data['data'].values()))

        df = pd.concat([x for x in coin_meta])
        df.columns = [x.replace('.', '_').replace('-','_') for x in list(df.columns)]
        df['urls_reddit'] = [x[0] if len(x) >0 else None for x in df.urls_reddit]
        df = df.reset_index(drop=True)
    
    return df


def init_db():
    df = get_coins()
    coins = df['id'].unique()

    df_meta = get_coin_meta(coins)


    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    coin = models.Coins()

    for row in df_meta.itertuples():
        db.add(models.Coins(
            id = row.id,
            symbol = row.symbol,
            name = row.name,
            slug = row.slug,
            date_added = pd.to_datetime(row.date_added),
            category = row.category,
            description = row.description,
            logo = row.logo,
            url_reddit = row.urls_reddit,
            platform_id = row.platform_id,
            platform_name = row.platform_name,
            platform_token_address = row.platform_token_address

        ))

    db.commit()


init_db()