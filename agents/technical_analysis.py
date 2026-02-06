import pandas as pd
import numpy as np
from database.models import Analysis, Price, get_session
from utils.helpers import logger, get_fibonacci_levels

def analyze_all_stocks():
    session = get_session()
    results = []
    
    logger.info("🔬 Starting technical analysis...")
    
    # جلب جميع الأسهم من قاعدة البيانات
    symbols = session.query(Price.symbol).distinct().all()
    symbols = [s[0] for s in symbols]
    
    for symbol in symbols:
        try:
            # جلب البيانات
            prices = session.query(Price).filter(
                Price.symbol == symbol
            ).order_by(Price.date.asc()).all()
            
            if len(prices) < 50:
                continue
            
            df = pd.DataFrame([{
                'date': p.date,
                'open': float(p.open),
                'high': float(p.high),
                'low': float(p.low),
                'close': float(p.close),
                'volume': p.volume
            } for p in prices])
            
            # حساب المؤشرات
            current = df['close'].iloc[-1]
            sma_20 = df['close'].rolling(20).mean().iloc[-1]
            sma_50 = df['close'].rolling(50).mean().iloc[-1]
            
            # RSI بسيط
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi = rsi.iloc[-1]
            
            # تحديد الاتجاه
            if current > sma_20 > sma_50:
                trend = "Strong Uptrend"
                signal = "BUY"
                score = 80
            elif current > sma_20:
                trend = "Uptrend"
                signal = "BUY"
                score = 70
            elif current < sma_20 < sma_50:
                trend = "Strong Downtrend"
                signal = "SELL"
                score = 30
            else:
                trend = "Sideways"
                signal = "HOLD"
                score = 50
            
            # الأهداف
            target_1 = current * 1.05
            target_2 = current * 1.10
            stop_loss = current * 0.95
            
            # حفظ التحليل
            analysis = Analysis(
                symbol=symbol,
                date=pd.Timestamp.now(),
                current_price=current,
                trend=trend,
                signal=signal,
                score=score,
                rsi=rsi,
                sma_20=sma_20,
                sma_50=sma_50,
                target_1=target_1,
                target_2=target_2,
                stop_loss=stop_loss
            )
            session.merge(analysis)
            session.commit()
            
            results.append({
                'symbol': symbol,
                'price': current,
                'signal': signal,
                'score': score,
                'trend': trend
            })
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
    
    logger.info(f"✅ Analysis completed for {len(results)} stocks")
    return sorted(results, key=lambda x: x['score'], reverse=True)

def get_top_picks(n=10):
    session = get_session()
    analyses = session.query(Analysis).order_by(Analysis.score.desc()).limit(n).all()
    return analyses