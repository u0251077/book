import streamlit as st
import pandas as pd

# 設置頁面配置
st.set_page_config(page_title="我的閱讀心得", layout="wide")

# 自定義CSS
st.markdown("""
<style>
    body {
        color: #333;
        background-color: white;
    }
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    .book-entry {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
    h1, h2 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# 標題
st.title("我的閱讀心得")

# 側邊欄用於添加新書籍
with st.sidebar:
    st.header("添加新書籍")
    new_book = st.text_input("書名")
    new_author = st.text_input("作者")
    new_thoughts = st.text_area("閱讀心得")
    if st.button("添加"):
        if new_book and new_author and new_thoughts:
            # 在這裡你可以將數據保存到文件或數據庫中
            st.success("成功添加新書籍!")
        else:
            st.error("請填寫所有字段")

# 主頁面顯示書籍列表
st.header("我的書籍列表")

# 這裡應該從某個數據源（如文件或數據庫）獲取書籍數據
# 為了演示，我們使用一個示例列表
books = [
    {"title": "1984", "author": "George Orwell", "thoughts": "一本發人深省的反烏托邦小說，讓我思考了很多關於言論自由和隱私的問題。"},
    {"title": "百年孤獨", "author": "加布里埃爾·加西亞·馬爾克斯", "thoughts": "魔幻現實主義的經典之作，家族史詩般的敘事手法令人印象深刻。"}
]

for book in books:
    with st.container():
        st.markdown(f"""
        <div class="book-entry">
            <h2>{book['title']}</h2>
            <p><strong>作者：</strong>{book['author']}</p>
            <p><strong>閱讀心得：</strong>{book['thoughts']}</p>
        </div>
        """, unsafe_allow_html=True)

# 互動功能：搜索
search_query = st.text_input("搜索書籍")
if search_query:
    filtered_books = [book for book in books if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower()]
    if filtered_books:
        st.write(f"搜索結果：找到 {len(filtered_books)} 本書")
        for book in filtered_books:
            st.write(f"- {book['title']} by {book['author']}")
    else:
        st.write("沒有找到匹配的書籍")
