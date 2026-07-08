import streamlit as st
import yfinance as yf
import pandas as pd

# Konfigurasi Page
st.set_page_config(page_title="Stock Swing Screener", layout="wide")

st.title("📈 Swing Trading Screener")
st.write("Mencari saham dengan tren naik dan volume tinggi.")

# Daftar saham (Bisa ditambah sesuai keinginan)
# Contoh: Saham-saham LQ45 populer
stock_list = ["BBCA.JK", "BBRI.JK", "TLKM.JK", "ASII.JK", "BMRI.JK", 
              "UNVR.JK", "GOTO.JK", "BBNI.JK", "ADRO.JK", "ICBP.JK"]

def scan_stocks(tickers):
    screened_data = []
    
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="1y", interval="1d", progress=False)
            if len(df) < 200: continue
            
            # Hitung Indikator
            df['SMA50'] = df['Close'].rolling(window=50).mean()
            df['SMA200'] = df['Close'].rolling(window=200).mean()
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Filter Logika
            is_uptrend = last['Close'] > last['SMA200']
            is_momentum = last['Close'] > last['SMA50']
            is_high_volume = last['Volume'] > (last['Vol_Avg'] * 1.1) # 10% di atas rata-rata
            
            if is_uptrend and is_momentum and is_high_volume:
                screened_data.append({
                    "Ticker": ticker,
                    "Price": round(float(last['Close']), 2),
                    "SMA50": round(float(last['SMA50']), 2),
                    "SMA200": round(float(last['SMA200']), 2)
                })
        except Exception as e:
            continue
            
    return pd.DataFrame(screened_data)

# Sidebar UI
if st.sidebar.button("Mulai Screening"):
    with st.spinner('Sedang memproses data dari Bursa...'):
        results = scan_stocks(stock_list)
        
        if not results.empty:
            st.success(f"Ditemukan {len(results)} saham yang cocok!")
            st.table(results)
        else:
            st.warning("Tidak ada saham yang memenuhi kriteria hari ini.")
else:
    st.info("Klik tombol di sidebar untuk mulai memindai saham.")

st.markdown("""
### Cara Kerja Filter:
* **Uptrend:** Harga > SMA 200.
* **Momentum:** Harga > SMA 50.
* **Volume:** Volume hari ini > 110% dari rata-rata volume 20 hari terakhir.
""")
