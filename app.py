import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 網頁初始設定：強制開啟寬螢幕、標題與小圖示
st.set_page_config(page_title="Phoebe 頂級投資儀表板", page_icon="📈", layout="wide")

# 2. 注入自訂高級 UI/UX CSS 樣式
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Helvetica, Arial, "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    div.stBox {
        border-radius: 12px;
        padding: 1.5rem;
        background-color: #1E293B;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38BDF8, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部精美標頭
st.markdown('<p class="main-title">📊 Phoebe 頂級投資儀表板</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">全球核心資產與原廠一手財報數據追蹤</p>', unsafe_allow_html=True)

# ==============================================================================
# SECTION 1: 美股大盤指標 VOO 觀測與買進評估
# ==============================================================================
st.markdown("### 🇺🇸 全球大盤核心觀測 (VOO)")

# 抓取 VOO 數據
voo_ticker = yf.Ticker("VOO")
voo_info = voo_ticker.info
voo_hist = voo_ticker.history(period="3mo")

if not voo_hist.empty:
    # 簡略計算日 KD (9, 3, 3) 用於買進參考
    low_9 = voo_hist['Low'].rolling(window=9).min()
    high_9 = voo_hist['High'].rolling(window=9).max()
    rsv = ((voo_hist['Close'] - low_9) / (high_9 - low_9)) * 100
    
    k_list = []
    d_list = []
    current_k = 50
    current_d = 50
    for r in rsv:
        if pd.isna(r):
            k_list.append(None)
            d_list.append(None)
        else:
            current_k = (2/3) * current_k + (1/3) * r
            current_d = (2/3) * current_d + (1/3) * current_k
            k_list.append(current_k)
            d_list.append(current_d)
            
    latest_k = current_k
    latest_d = current_d
    
    # 計算漲跌
    current_price = voo_hist['Close'].iloc[-1]
    prev_price = voo_hist['Close'].iloc[-2]
    price_change = current_price - prev_price
    price_change_pct = (price_change / prev_price) * 100
    
    # 決定買進建議資訊
    if latest_k < 20:
        action_status = "🔥 買進訊號強烈 (KD低檔超賣)"
        action_color = "red"
        action_desc = "目前 VOO 技術指標處於低檔相對安全區，通常為中長期投資人進場的黃金時機。"
    elif latest_k > 80:
        action_status = "⚠️ 暫緩追高 (KD高檔超買)"
        action_color = "orange"
        action_desc = "目前技術指標處於高檔過熱區，建議若無急迫性可靜待拉回再布局。"
    else:
        action_status = "⚖️ 穩定配置區 (KD訊號中性)"
        action_color = "green"
        action_desc = "目前指數運作正常，處於合理波動範圍。適合實施定時定額或按原計畫分批布局。"

    # VOO 資訊卡片區
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        st.metric(
            label="VOO 最新股價", 
            value=f"${current_price:.2f}", 
            delta=f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
        )
    with c2:
        st.metric(
            label="技術指標 (日K / 日D)", 
            value=f"{latest_k:.1f} / {latest_d:.1f}"
        )
    with c3:
        st.markdown(
            f"""
            <div style="background-color: #0F172A; border-left: 5px solid {action_color}; padding: 12px; border-radius: 6px;">
                <b style="font-size: 1.1rem; color: white;">目前操作評估：{action_status}</b><br>
                <span style="font-size: 0.9rem; color: #94A3B8;">{action_desc}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
else:
    st.error("無法取得 VOO 即時數據，請稍後再試。")

st.markdown("<br><hr style='border-color: #334155;'><br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: 個股原廠第一手財報數據
# ==============================================================================
st.markdown("### 🔍 個股原廠第一手數據查詢")

ticker_input = st.text_input("請輸入股票代號 (台股請加 .TW，例如：2330.TW)", "2330.TW")
ticker = yf.Ticker(ticker_input)

# 基本面核心三大數字指標
try:
    info = ticker.info
    if info:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("目前本益比 (PE)", f"{info.get('trailingPE', '暫無')}")
        with m2:
            st.metric("每股盈餘 (EPS)", f"${info.get('trailingEps', '暫無')}")
        with m3:
            st.metric("利潤率 (Profit Margin)", f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else "暫無")
        with m4:
            st.metric("股東權益報酬率 (ROE)", f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else "暫無")
except:
    st.warning("部分即時核心指標暫時無法讀取。")

# 官方檔案下載直達車
pure_code = ticker_input.split(".")[0]
st.markdown("#### 📂 官方原始檔案直達鏈結")
col_link1, col_link2 = st.columns(2)
with col_link1:
    st.markdown(f"**🏢 台灣公開資訊觀測站 (MOPS)**\n\n[👉 點我直接進入官方網站查重大訊息](https://mops.twse.com.tw/mops/web/t05st01)")
with col_link2:
    st.markdown(f"**📊 官方法說會簡報 (Investor Relations)**\n\n[👉 點我直接 Google 搜尋原廠 PDF 簡報](https://www.google.com/search?q={pure_code}+Investor+Relations+法說會簡報+filetype:pdf)")

# 原始大數據表格分頁
st.markdown("#### 🏛️ 申報原始財務三表 (無任何加工處理)")
tab1, tab2, tab3 = st.tabs(["損益表 (Income Statement)", "資產負債表 (Balance Sheet)", "現金流量表 (Cash Flow)"])

with tab1:
    st.dataframe(ticker.quarterly_financials, use_container_width=True)
with tab2:
    st.dataframe(ticker.quarterly_balance_sheet, use_container_width=True)
with tab3:
    st.dataframe(ticker.quarterly_cashflow, use_container_width=True)
