import streamlit as st

# 設置頁面配置
st.set_page_config(page_title="我的閱讀心得", layout="wide")

# 自定義CSS
st.markdown("""
<style>
    body {
        color: #333;
        background-color: white;
        font-family: Arial, sans-serif;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .book-entry {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .book-title {
        color: #2c3e50;
        font-size: 24px;
        margin-bottom: 10px;
        cursor: pointer;
    }
    .book-author {
        color: #7f8c8d;
        font-style: italic;
        margin-bottom: 10px;
    }
    .book-cover {
        width: 120px;
        height: 180px;
        object-fit: cover;
        float: left;
        margin-right: 20px;
        border-radius: 5px;
    }
    .book-content {
        overflow: hidden;
    }
    .book-thoughts {
        margin-top: 10px;
        display: none;
    }
    .expanded .book-thoughts {
        display: block;
    }
</style>

<script>
function toggleContent(id) {
    var element = document.getElementById(id);
    element.classList.toggle("expanded");
}
</script>
""", unsafe_allow_html=True)

# 標題
st.markdown("<h1 style='text-align: center;'>我的閱讀心得</h1>", unsafe_allow_html=True)

# 書籍數據
books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "cover": "https://via.placeholder.com/120x180.png?text=1984",
        "thoughts": "一本發人深省的反烏托邦小說，讓我思考了很多關於言論自由和隱私的問題。這本書描繪了一個極權主義社會，其中的人民被剝奪了思考和表達的自由。通過主角溫斯頓·史密斯的經歷，我們看到了人性在極端壓迫下的掙扎和反抗。這本書對於理解現代社會中的監控問題和個人隱私權有著深遠的影響。"
    },
    {
        "id": 2,
        "title": "百年孤獨",
        "author": "加布里埃爾·加西亞·馬爾克斯",
        "cover": "https://via.placeholder.com/120x180.png?text=百年孤獨",
        "thoughts": "魔幻現實主義的經典之作，家族史詩般的敘事手法令人印象深刻。這本書講述了布恩迪亞家族七代人的故事，通過他們的生活展現了拉丁美洲的歷史和文化。馬爾克斯的寫作風格將現實與幻想完美融合，創造出一個豐富多彩、充滿神奇色彩的世界。這本書讓我深刻體會到了人類命運的循環性和孤獨的普遍性。"
    }
]

# 顯示書籍列表
for book in books:
    st.markdown(f"""
    <div class="book-entry" id="book-{book['id']}">
        <img src="{book['cover']}" alt="{book['title']} 封面" class="book-cover">
        <div class="book-content">
            <h2 class="book-title" onclick="toggleContent('book-{book['id']}')">{book['title']}</h2>
            <p class="book-author">作者：{book['author']}</p>
            <div class="book-thoughts">{book['thoughts']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<script>
    // 由於Streamlit的限制，這個腳本可能不會執行。
    // 您可能需要使用Streamlit組件或其他方法來實現交互性。
</script>
""", unsafe_allow_html=True)
