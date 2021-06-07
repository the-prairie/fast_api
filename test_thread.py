from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time
from pytrends.request import TrendReq

def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


coins = ['BTC',
 'ETH',
 'USDT',
 'BNB',
 'ADA',
 'DOGE',
 'XRP',
 'USDC',
 'DOT',
 'UNI',
 'ICP',
 'BCH',
 'LINK',
 'LTC',
 'SOL',
 'MATIC',
 'BUSD',
 'THETA',
 'XLM',
 'VET',
 'ETC',
 'WBTC',
 'FIL',
 'EOS',
 'TRX',
 'XMR',
 'DAI',
 'AAVE',
 'NEO',
 'MKR',
 'KSM',
 'MIOTA',
 'SHIB',
 'CAKE',
 'KLAY',
 'BSV',
 'FTT',
 'ATOM',
 'CRO',
 'ALGO',
 'HT',
 'BTT',
 'BTCB',
 'LEO',
 'LUNA',
 'TFUEL'] # 16 urls

def load_trends(coin):  
    pytrend = TrendReq()
    kw_list =  [coins[coin]]
    pytrend.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='')
    
    return pytrend.interest_over_time()
  


n_jobs = len(coins)


n_threads = 16
marker = time.time()
d = multithreading(load_trends, range(n_jobs), n_threads)
print("Multithreading {} spent".format(n_threads), time.time() - marker)

print(d)