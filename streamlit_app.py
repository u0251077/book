import streamlit as st
import pandas as pd
import altair as alt

# 固定活動數據
data = {
    "等級": [207, 207],
    "活動名稱": ["湯寶寶", "次元入侵"],
    "時間（分鐘）": [2, 3],
    "經驗值": [251360181, 2000000000],
}

# 將數據轉換為DataFrame
df = pd.DataFrame(data)

# 計算每個活動的CP值
df["CP值（經驗/時間）"] = df["經驗值"] / df["時間（小時）"]

# Streamlit 標題
st.title("遊戲活動CP值分析")

# Streamlit 描述
st.write("""
這個頁面展示了不同活動在不同等級下的花費時間、獲得的經驗值以及對應的性價比（CP值）。
性價比越高，活動越值得優先進行。數據已寫死，僅供展示用途。
""")

# 創建選擇框來選擇等級
selected_level = st.selectbox("選擇等級", df["等級"].unique())

# 過濾選擇的等級的數據
filtered_df = df[df["等級"] == selected_level]

# 顯示該等級的活動數據
st.write(f"### 等級 {selected_level} 的活動分析")
st.dataframe(filtered_df)

# 按照CP值排序後顯示
sorted_df = filtered_df.sort_values(by="CP值（經驗/時間）", ascending=False)
st.write(f"### 等級 {selected_level} 的CP值排序")
st.dataframe(sorted_df)

# 使用 Altair 繪製條形圖來可視化 CP 值
st.write(f"### 等級 {selected_level} 的CP值視覺化")

chart = alt.Chart(sorted_df).mark_bar().encode(
    x=alt.X('活動名稱', sort=None, title='活動名稱'),
    y=alt.Y('CP值（經驗/時間）', title='CP值 (經驗 / 時間)'),
    tooltip=['活動名稱', '時間（小時）', '經驗值', 'CP值（經驗/時間）']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

st.altair_chart(chart, use_container_width=True)

# 可選：繪製所有等級的CP值趨勢圖
st.write("### 各等級下活動的CP值趨勢")

trend_chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('等級', title='等級'),
    y=alt.Y('CP值（經驗/時間）', title='CP值 (經驗 / 時間)'),
    color='活動名稱',
    tooltip=['等級', '活動名稱', 'CP值（經驗/時間）']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

st.altair_chart(trend_chart, use_container_width=True)
