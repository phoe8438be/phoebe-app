import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 網頁初始設定：可愛圖示與寬螢幕
st.set_page_config(page_title="Phoebe 的理財秘密花園", page_icon="🌸", layout="wide")

# 初始化日誌儲存空間
if "diary_logs" not in st.session_state:
    st.session_state.diary_logs = {
        "2026-06-12": {
            "note": "今天看盤發現大盤在高檔震盪，還是要聽話，定時定額不亂追高！",
            "reply": "🐾 AI 小熊評語：做得太棒了！市場震盪時保持冷靜是最高級的智慧，給妳蓋一個乖乖章！ hard-working Phoebe! 🧸"
        }
    }

# 2. 注入繽紛可愛又易讀的馬卡龍 UI/UX 樣式
st.markdown("""
    <style>
    /* 全域可愛字體與背景 */
    html, body, [class*="css"] {
        font-family: "Comic Sans MS", "Chalkboard SE", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    /* 可愛果凍圓角區塊 */
    .cute-card {
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        border: None;
        box-shadow: 0 8px 16px rgba(0,0,0,0,05);
    }
    .pink-card { background-color: #FFF0F5; border-left: 8px solid #FF69B4; }     /* 櫻花粉 */
    .green-card { background-color: #F0FFF4; border-left: 8px solid #48BB78; }    /* 薄荷綠 */
    .blue-card { background-color: #EBF8FF; border-left: 8px solid #4299E1; }     /* 天空藍 */
    .yellow-card { background-color: #FEFCBF; border-left: 8px solid #ECC94B; }   /* 蜂蜜黃 */
    .purple-card { background-color: #FAF5FF; border-left: 8px solid #9F7AEA; }   /* 薰衣草紫 */
    
    /* 繽紛標題 */
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #FF1493;
        text-shadow: 2px 2px #FFD1DC;
        margin-bottom: 0.2rem;
    }
    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #2D3748;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部迎賓
st.markdown('<p class="main-title">🌸 Phoebe 的理財秘密花園 🌸</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #718096; font-size: 1.1rem; margin-bottom: 2rem;">跟著數據快樂成長，拒絕生硬火星文！✨</p>', unsafe_allow_html=True)

# 建立四大繽紛分頁
tab_voo, tab_industry, tab_stock, tab_diary = st.tabs([
    "🇺🇸 蜜糖美股 VOO", 
    "📰 每日必看產業特輯", 
    "🔍 台灣個股小白健檢", 
    "✍️ 每日看盤學習日記"
])

# ==============================================================================
# TAB 1: 蜜糖美股 VOO 獨立頁面
# ==============================================================================
with tab_voo:
    st.markdown('<p class="section-title">🍓 美股大盤 VOO 觀測站</p>', unsafe_allow_html=True)
    
    voo = yf.Ticker("VOO")
    h = voo.history(period="3mo")
    
    if not h.empty:
        price = h['Close'].iloc[-1]
        change = price - h['Close'].iloc[-2]
        pct = (change / h['Close'].iloc[-2]) * 100
        
        # 計算簡易日KD
        low_9 = h['Low'].rolling(window=9).min()
        high_9 = h['High'].rolling(window=9).max()
        rsv = ((h['Close'] - low_9) / (high_9 - low_9)) * 100
        k = 50
        for r in rsv.dropna():
            k = (2/3) * k + (1/3) * r
            
        # 決定甜美買進小提示
        if k < 25:
            hint_box = '<div class="cute-card pink-card"><h3>💖 甜甜價來了！(K值超低)</h3>現在大盤跌入特價區，如果是定期定額或想撿便宜的女孩，現在是個分批買進的超棒黃金時機喔！</div>'
        elif k > 75:
            hint_box = '<div class="cute-card yellow-card"><h3>🥞 點心時間，先別追高！(K值偏高)</h3>現在股市有點過熱囉，像是剛出爐的鬆餅太燙了！建議手癢想買的話先忍忍，拉回再抱它。</div>'
        else:
            hint_box = '<div class="cute-card blue-card"><h3>🌱 氣候宜人，穩定存股區</h3>目前價格很安全、不貴也不便宜。最適合維持原計畫「乖乖定期定額」，不知不覺就會累積大財富！</div>'
            
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🍦 VOO 今日最新價", value=f"${price:.2f} USD", delta=f"{change:+.2f} ({pct:+.2f}%)")
        with col2:
            st.metric(label="🎯 體感熱度 (K值)", value=f"{k:.1f} °C")
            
        st.markdown(hint_box, unsafe_allow_html=True)
        
        # AI 導師針對 VOO 的直接意見
        st.markdown(f"""
        <div class="cute-card purple-card">
            <h4>🤖 AI 私人蜜糖導師開示：</h4>
            <p>VOO 代表的是全美國最強的 500 家公司（包含 Apple、微軟、特斯拉等）。妳買一張 VOO 就等於讓這些世界頂尖菁英幫妳打工。
            目前最新價格在 <b>${price:.2f}</b>，長期看來人類科技只會不斷進步，所以不需要在意每天的碎步波動，<b>只要特價訊號亮起就多買一點</b>，妳的資產就會像滾雪球一樣越來越大！</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: 每日必看產業特輯 (不用自己喂 Google 囉！)
# ==============================================================================
with tab_industry:
    st.markdown('<p class="section-title">🍍 每天必讀！核心產業第一手重點</p>', unsafe_allow_html=True)
    st.write("不必再去大海撈針看一堆廢話新聞！每天進來，直接吸收目前市場上最關鍵的黃金產業風向：")
    
    st.markdown("""
    <div class="cute-card green-card">
        <h3>🧠 1. AI 與半導體產業 (護國神山供應鏈)</h3>
        <ul>
            <li><b>必看核心：</b> 關注「台積電營收公告」與「輝達 (NVIDIA) 晶片出貨量」。</li>
            <li><b>女孩直白翻譯：</b> 全世界的科技產品、AI機器人全部都要用台積電做的晶片。只要台積電每個月公布的營收是成長的，整個半導體行情就不會冷，這叫原廠底氣。</li>
        </ul>
    </div>
    
    <div class="cute-card blue-card">
        <h3>⚡ 2. 綠能與重電產業 (台灣本土剛性需求)</h3>
        <ul>
            <li><b>必看核心：</b> 關注「台電強韌電網計畫發包」與「半導體大廠綠能採購」。</li>
            <li><b>女孩直白翻譯：</b> 台灣不管是蓋科學園區還是日常吹冷氣，電永遠不夠用！這群做重電設備、電纜、太陽能的公司，訂單早就排到好幾年後，屬於政策一條鞭保護的穩健產業。</li>
        </ul>
    </div>
    
    <div class="cute-card yellow-card">
        <h3>🚢 3. 航運與全球供應鏈 (景氣調味劑)</h3>
        <ul>
            <li><b>必看核心：</b> 關注「SCFI 運價指數」與「地緣政治國際運河衝突」。</li>
            <li><b>女孩直白翻譯：</b> 貨物塞在海上，運費就會暴漲，航運股就會瘋狂噴發。但這種產業變動像天氣一樣快，賺得快跌得也快，適合心臟大顆時觀察，不適合當作主力存股喔！</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: 台灣個股小白健檢 (看不懂財報別怕，AI 把火星文翻成白話文)
# ==============================================================================
with tab_stock:
    st.markdown('<p class="section-title">🍭 台灣個股原廠核心白話翻譯</p>', unsafe_allow_html=True)
    
    t_input = st.text_input("請輸入你想健檢的台股代號（例如台積電：2330.TW）", "2330.TW", key="stock_check")
    tk = yf.Ticker(t_input)
    
    try:
        info = tk.info
        if info:
            pe = info.get('trailingPE', '暫無')
            eps = info.get('trailingEps', '暫無')
            margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
            roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
            
            # 可愛四大指標卡片
            c_a, c_b, c_c, c_d = st.columns(4)
            with c_a: st.metric("🍒 賺錢效率 (ROE)", f"{roe:.2f}%")
            with c_b: st.metric("🍯 純利潤率 (Margin)", f"{margin:.2f}%")
            with c_c: st.metric("💎 每股賺多少 (EPS)", f"${eps}")
            with c_d: st.metric("⏳ 幾年回本 (PE)", f"{pe}年")
            
            # 🧁 財報火星文大翻譯 (消滅看不懂的表格)
            st.markdown(f"""
            <div class="cute-card pink-card">
                <h3>🧁 Phoebe 專屬：原廠三大數字白話翻譯</h3>
                <ol>
                    <li><b>這家公司會賺錢嗎？（看ROE）：</b> 目前這家公司的 ROE 是 <b>{roe:.2f}%</b>！意思是他拿股東的 100 塊去投資，能賺回 {roe:.2f} 塊。通常只要 <b>ROE > 15%</b> 就是天生賺錢機器的優秀好公司！</li>
                    <li><b>產品利潤高嗎？（看純利潤率）：</b> 產品利潤率為 <b>{margin:.2f}%</b>。這代表扣掉所有材料、員工薪水，每賣出 100 塊還能淨賺 {margin:.2f} 塊！利潤越高，代表對手越無法複製它。</li>
                    <li><b>現在買會太貴嗎？（看本益比PE）：</b> 目前本益比是 <b>{pe}</b>。白話意思就是「如果公司維持現在的賺錢速度，妳買進後大約需要 <b>{pe} 年</b>能完全回本」。數字越低代表越便宜！</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            # 補回 AI 提供的主動意見
            st.markdown(f"""
            <div class="cute-card purple-card">
                <h4>🤖 AI 私人導師對 {t_input} 的綜合體檢意見：</h4>
                <p>這家公司的 ROE 表現和利潤率已經毫無保留地展現了它的原廠實力。拒絕看雜亂的新聞，妳直接看這兩個數字就夠了！
                如果 <b>ROE 持續大於 15%</b> 且 <b>利潤率穩定</b>，這就是癌大常說的「優質資產」。只要在股價拉回、本益比降低時默默分批布局，時間拉長，市場一定會給妳豐厚的回報！</p>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error("輸入錯誤或目前無法抓取該股票原始基本面數據。")

# ==============================================================================
# TAB 4: 每日看盤學習日記 (有日期、可回溯、可愛版面與 AI 回應)
# ==============================================================================
with tab_diary:
    st.markdown('<p class="section-title">📝 Phoebe 的每日股市學習日記</p>', unsafe_allow_html=True)
    
    # 1. 填寫新日記區（預設抓今天日期）
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    st.markdown(f"""
    <div class="cute-card yellow-card">
        <h4>🎈 今天是：{today_str} (新日記本)</h4>
        <p>親愛的 Phoebe，今天在市場上有學到什麼、或是觀察到什麼好玩的心得嗎？記錄下來吧！</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_note = st.text_area("在這裡寫下今天的觀察筆記...", placeholder="例如：今天 VOO 亮起綠燈，我定時定額加碼了扣款！或者是今天忍住沒追高某檔熱門股。")
    
    if st.button("🌸 寫好日記了，送出給小熊評分！"):
        if user_note.strip() != "":
            # 簡單模擬一個可愛的 AI 動態回應
            ai_reply = f"🐾 AI 小熊評語：哇！讀完妳今天 ({today_str}) 的筆記，覺得 Phoebe 對市場越來越有盤感了呢！懂得看指標和控制情緒，妳已經打敗市場上 80% 亂衝的人了。繼續保持這種原廠數據流的理性操作，累積久了，妳的資產一定會像小熊的蜂蜜罐一樣滿出來喔！🧸✨"
            
            # 儲存到 session_state 中
            st.session_state.diary_logs[today_str] = {
                "note": user_note,
                "reply": ai_reply
            }
            st.success("🎉 日記成功收進保險箱囉！")
        else:
            st.warning("請先寫點字再送出喔～")
            
    st.write("---")
    
    # 2. 歷史日記回溯區
    st.markdown("#### 📜 翻閱過去的學習紀錄 (回溯歷史)")
    
    if st.session_state.diary_logs:
        # 讓使用者下拉選單選擇想要回溯哪一天的日記
        available_dates = sorted(list(st.session_state.diary_logs.keys()), reverse=True)
        selected_date = st.selectbox("請選擇想查看的歷史日期：", available_dates)
        
        # 顯示被回溯那一天的內容
        past_data = st.session_state.diary_logs[selected_date]
        st.markdown(f"""
        <div class="cute-card blue-card">
            <h5>📅 {selected_date} 妳寫下的筆記：</h5>
            <p style="color: #2D3748; font-size: 1.05rem;"><i>「 {past_data['note']} 」</i></p>
            <hr style="border-color: #CBD5E0;">
            <p style="color: #6B46C1; font-weight: bold;">{past_data['reply']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("目前還沒有任何歷史紀錄喔，快寫下第一篇吧！")
