import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional
import ta

# Constants and Configuration
CURRENCIES = {
    'TWD': '新台幣',
    'USD': '美元',
    'HKD': '港幣'
}

# Page configuration
st.set_page_config(
    page_title="金融資產追蹤儀表板",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .news-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00ff00;
    }
    </style>
""", unsafe_allow_html=True)

# Caching functions
@st.cache_data(ttl=3600)
def get_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """下載股票歷史數據"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        st.error(f"獲取股票數據時發生錯誤: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_exchange_rates(base: str, targets: List[str]) -> Dict[str, float]:
    """獲取即時匯率"""
    rates = {}
    for target in targets:
        if base != target:
            ticker = f"{base}{target}=X"
            try:
                rate = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
                rates[target] = rate
            except:
                rates[target] = 1.0
    return rates

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """計算技術指標"""
    # 移動平均線
    df['MA20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['MA50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['MA200'] = ta.trend.sma_indicator(df['Close'], window=200)
    
    # RSI
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # 布林通道
    indicator_bb = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
    df['BB_upper'] = indicator_bb.bollinger_hband()
    df['BB_lower'] = indicator_bb.bollinger_lband()
    df['BB_middle'] = indicator_bb.bollinger_mavg()
    
    return df

def create_candlestick_chart(df: pd.DataFrame, show_volume: bool = True) -> go.Figure:
    """創建K線圖"""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.03, row_heights=[0.7, 0.3])

    # K線圖
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='K線'
    ), row=1, col=1)

    # 技術指標
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20',
                            line=dict(color='yellow', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50',
                            line=dict(color='blue', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], name='MA200',
                            line=dict(color='red', width=1)), row=1, col=1)

    # 布林通道
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name='BB上軌',
                            line=dict(color='gray', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name='BB下軌',
                            line=dict(color='gray', width=1, dash='dash')), row=1, col=1)

    # 成交量
    if show_volume:
        colors = ['red' if row['Open'] - row['Close'] >= 0 
                 else 'green' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
                            name='成交量',
                            marker_color=colors,
                            marker_line_color=colors,
                            marker_line_width=1.5), row=2, col=1)

    # 更新版面設置
    fig.update_layout(
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        height=800,
        title_text="股票技術分析圖表",
        showlegend=True
    )

    return fig

def calculate_portfolio_metrics(df: pd.DataFrame, investment_amount: float) -> Dict[str, float]:
    """計算投資組合指標"""
    # 計算日報酬率
    df['Returns'] = df['Close'].pct_change()
    
    # 年化報酬率
    annual_return = ((1 + df['Returns'].mean()) ** 252 - 1) * 100
    
    # 年化波動率
    annual_volatility = df['Returns'].std() * np.sqrt(252) * 100
    
    # 夏普比率 (假設無風險利率為2%)
    risk_free_rate = 0.02
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    
    # 最大回撤
    cumulative_returns = (1 + df['Returns']).cumprod()
    rolling_max = cumulative_returns.expanding().max()
    drawdowns = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = drawdowns.min() * 100
    
    return {
        "年化報酬率": annual_return,
        "年化波動率": annual_volatility,
        "夏普比率": sharpe_ratio,
        "最大回撤": max_drawdown
    }

def main():
    # Sidebar設置
    st.sidebar.title("設置")
    selected_stocks = st.sidebar.multiselect(
        "選擇股票",
        ["VWRA.L", "IWDA.L", "EIMI.L"],
        default=["VWRA.L"]
    )
    
    time_period = st.sidebar.selectbox(
        "時間區間",
        ["1m", "3m", "6m", "1y", "2y", "5y"],
        index=3
    )
    
    display_currency = st.sidebar.selectbox(
        "顯示幣別",
        list(CURRENCIES.keys()),
        format_func=lambda x: CURRENCIES[x]
    )

    # 主頁面
    st.title("金融資產追蹤儀表板")
    
    # 獲取數據
    for stock in selected_stocks:
        st.header(f"{stock} 分析")
        
        # 獲取股票數據
        df = get_stock_data(stock, time_period)
        if df.empty:
            continue
            
        # 計算技術指標
        df = calculate_technical_indicators(df)
        
        # 分析指標
        col1, col2, col3, col4 = st.columns(4)
        metrics = calculate_portfolio_metrics(df, 10000)  # 假設投資金額
        
        with col1:
            st.metric("年化報酬率", f"{metrics['年化報酬率']:.2f}%")
        with col2:
            st.metric("年化波動率", f"{metrics['年化波動率']:.2f}%")
        with col3:
            st.metric("夏普比率", f"{metrics['夏普比率']:.2f}")
        with col4:
            st.metric("最大回撤", f"{metrics['最大回撤']:.2f}%")
        
        # K線圖
        fig = create_candlestick_chart(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # 技術指標面板
        with st.expander("技術指標詳情"):
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df['RSI'])
            with col2:
                st.line_chart(df[['BB_upper', 'BB_middle', 'BB_lower']])

        # 交易記錄
        st.subheader("交易記錄")
        transaction_data = pd.DataFrame({
            "日期": ["2024/08/06", "2024/09/05"],
            "交易類型": ["買入", "買入"],
            "成交價格": [126.46, 134.08],
            "成交數量": [12, 1],
            "手續費": [3.79, 0.336],
            "總成本": [1521.31, 134.416],
            "幣別": ["USD", "USD"]
        })
        
        st.dataframe(
            transaction_data.style.format({
                '成交價格': '${:,.2f}',
                '手續費': '${:,.2f}',
                '總成本': '${:,.2f}'
            })
        )

if __name__ == "__main__":
    main()
