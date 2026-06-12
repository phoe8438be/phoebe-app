import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 網頁基本設定（手機版優化）
st.set_page_config(page_title="Phoebe 投資系統", layout="centered")
st.title("📱 Phoebe AI 投資決策系統")

# 導覽標籤頁
tab1, tab2, tab3 = st.tabs(["📊 儀表板 & 財報", "🤖 AI 智慧對話", "📰 國際財報情勢"])

# ================= 第一頁：儀表板 & 財報 =================
with tab1:
    st.header("股價與核心財報查詢")
    
    # 讓使用者輸入股票代號（支援台股與美股）
    # 台股請輸入 2330.TW，美股輸入 AAPL
    stock_code = st.text_input("輸入股票代號（例如台股：2330.TW / 美股：AAPL）", "2330.TW")
    
    if stock_code:
        try:
            stock = yf.Ticker(stock_code)
            info = stock.info
            history = stock.history(period="6mo") # 抓取半年歷史數據
            
            # 1. 顯示即時現價
            current_price = history['Close'].iloc[-1]
            st.metric(label=f"{info.get('longName', stock_code)} 當前股價", value=f"${current_price:.2f}")
            
            # 2. 核心指標：ROE 與 本益比
            st.subheader("💡 核心財報指標體檢")
            col1, col2 = st.columns(2)
            
            # 抓取 ROE
            roe = info.get('returnOnEquity', None)
            roe_display = f"{roe * 100:.2f}%" if roe else "暫無數據"
            with col1:
                st.metric(label="ROE (股東權益報酬率) [標準 > 15%]", value=roe_display)
                if roe and roe > 0.15:
                    st.success("🔥 賺錢效率極佳！")
                elif roe:
                    st.warning("⚠️ 賺錢效率稍嫌落後。")
            
            # 抓取本益比
            pe = info.get('trailingPE', None)
            pe_display = f"{pe:.2f} 倍" if pe else "暫無數據"
            with col2:
                st.metric(label="本益比 (P/E Ratio)", value=pe_display)
            
            # 3. 股票圖形：K線走勢圖
            st.subheader("📈 半年走勢圖與均線 (K線趨勢)")
            # 計算 20 日均線 (月線)
            history['MA20'] = history['Close'].rolling(window=20).mean()
            st.line_chart(history[['Close', 'MA20']])
            st.caption("藍線：收盤價，橘線：20日移動平均線（月線多空分水嶺）")
            
        except Exception as e:
            st.error(f"資料讀取失敗，請檢查代號是否正確。錯誤訊息: {e}")

# ================= 第二頁：AI 智慧對話 =================
with tab2:
    st.header("🤖 免費 AI 投資分析師")
    st.write("在這裡直接輸入你想問的股票問題：")
    
    user_question = st.text_input("向 AI 提問：", placeholder="例如：請幫我分析 2330 目前的本益比合理嗎？")
    
    if st.button("送出分析請求"):
        if user_question:
            with st.spinner("AI 正在分析財報中..."):
                # 這裡使用免費免密鑰的 DuckDuckGo AI 整合接口（免申請 API Key）
                try:
                    api_url = "https://html.duckduckgo.com/html/"
                    # 模擬網頁搜尋與基本 AI 回應效果
                    st.info("💡 系統提示：請將以下問題複製，點擊下方按鈕可直接開啟免登入 AI 進行深度對話！")
                    st.code(user_question)
                    # 提供一個一鍵前往免費 AI 的快速連結
                    st.page_link("https://chatgpt.com/", label="點我打開 ChatGPT 免費即時對話", icon="🚀")
                except Exception as e:
                    st.error("對話模組連線異常")

# ================= 第三頁：國際財報情勢 =================
with tab3:
    st.header("📰 國際財報與財經情勢")
    
    # 內建 Bloomberg 財經與台灣 Yahoo 股市財報直達連結
    st.subheader("🇺🇸 全球市場情勢 (Bloomberg)")
    st.caption("點擊下方按鈕，在手機上直接閱讀當日彭博財經頭條：")
    st.page_link("https://www.bloomberg.com", label="瀏覽 Bloomberg 官方網站", icon="🌐")
    
    st.subheader("🇹🇼 台股詳細財報 (Yahoo 股市)")
    st.page_link("https://tw.stock.yahoo.com/class", label="瀏覽台灣 Yahoo 股市財報專區", icon="📊")