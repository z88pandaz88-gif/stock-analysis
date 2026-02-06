import requests
import pandas as pd
from database.models import Price, get_session
from utils.config import TWELVE_DATA_API_KEY, EGYPTIAN_STOCKS
from utils.helpers import logger
import time

def collect_all_data():
    session = get_session()
    success = []
    failed = []
    
    logger.info(f"🚀 Starting data collection for {len(EGYPTIAN_STOCKS)} stocks...")
    
    for i, symbol in enumerate(EGYPTIAN_STOCKS, 1):
        try:
            logger.info(f"[{i}/{len(EGYPTIAN_STOCKS)}] Collecting {symbol}...")
            
            url = "https://api.twelvedata.com/time_series"
            params = {
                'symbol': f"{symbol}.EGX",
                'interval': '1day',
                'outputsize': 5000,
                'apikey': TWELVE_DATA_API_KEY
            }
            
            response = requests.get(url, timeout=30)
            data = response.json()
            
            if 'values' not in data or not data['values']:
                logger.warning(f"No data for {symbol}")
                failed.append(symbol)
                continue
            
            df = pd.DataFrame(data['values'])
            df['datetime'] = pd.to_datetime(df['datetime'])
            
            for _, row in df.iterrows():
                price = Price(
                    symbol=symbol,
                    date=row['datetime'],
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=int(float(row['volume']))
                )
                session.merge(price)
            
            session.commit()
            success.append(symbol)
            logger.info(f"✅ {symbol}: {len(df)} rows saved")
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"❌ {symbol}: {e}")
            failed.append(symbol)
    
    logger.info(f"✅ Completed: {len(success)} success, {len(failed)} failed")
    return {'success': success, 'failed': failed}