import streamlit as st
import base64

# 設置頁面配置
st.set_page_config(page_title="我的閱讀筆記", layout="wide")

# 自定義CSS和JS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');
    
    body {
        font-family: 'Noto Sans TC', sans-serif;
        background-color: #f0f4f8;
        color: #333;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 2em;
    }
    .book-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    .book-card:hover {
        transform: translateY(-5px);
    }
    .book-cover {
        width: 100%;
        height: 400px;
        object-fit: cover;
    }
    .book-info {
        padding: 1.5em;
    }
    .book-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .book-author {
        color: #7f8c8d;
        font-style: italic;
        margin-bottom: 1em;
    }
    .book-thoughts {
        font-size: 0.9em;
        line-height: 1.6;
    }
    .read-more {
        display: inline-block;
        margin-top: 1em;
        color: #3498db;
        cursor: pointer;
    }
</style>

<script>
function toggleThoughts(id) {
    var thoughts = document.getElementById('thoughts-' + id);
    var link = document.getElementById('link-' + id);
    if (thoughts.style.display === 'none' || thoughts.style.display === '') {
        thoughts.style.display = 'block';
        link.innerHTML = '收起';
    } else {
        thoughts.style.display = 'none';
        link.innerHTML = '閱讀更多';
    }
}
</script>
""", unsafe_allow_html=True)

# 模擬書籍數據
books = [
    {
        "id": 1,
        "title": "哈利波特與魔法石",
        "author": "J.K. 羅琳",
        "cover": "https://via.placeholder.com/400x600.png?text=哈利波特與魔法石",
        "thoughts": "這本書開啟了一個魔法世界的大門，讓我感受到了想像力的無窮魅力。哈利波特的冒險不僅僅是一個男孩的成長故事，更是關於友誼、勇氣和選擇的深刻寓言。羅琳筆下的霍格華茲魔法學校充滿了奇思妙想，每個角色都栩栩如生。這本書教會了我，即使在最黑暗的時刻，只要有希望和勇氣，我們也能找到光明。"
    },
    {
        "id": 2,
        "title": "三體",
        "author": "劉慈欣",
        "cover": "https://via.placeholder.com/400x600.png?text=三體",
        "thoughts": "《三體》是一部震撼人心的科幻巨作，它不僅展現了宏大的宇宙觀，還深入探討了人性的複雜性。劉慈欣以獨特的視角審視人類文明的脆弱性和宇宙文明間的殘酷競爭。書中對科技發展、哲學思考和人類命運的描述令人深思。通過地球文明面對外星威脅的故事，我更深刻地理解了人類在宇宙中的渺小，同時也感受到了人類意志的偉大。"
    },
    {
        "id": 3,
        "title": "百年孤獨",
        "author": "加布里埃爾·加西亞·馬爾克斯",
        "cover": "https://via.placeholder.com/400x600.png?text=百年孤獨",
        "thoughts": "馬爾克斯的《百年孤獨》是一部魔幻現實主義的經典之作。通過布恩迪亞家族七代人的故事，書中呈現了拉丁美洲的歷史縮影和人性的複雜面貌。這本書的敘事方式獨特，將現實與幻想、個人命運與歷史進程巧妙地交織在一起。閱讀過程中，我彷彿置身於馬孔多這個虛構小鎮，感受到了時間的流逝和命運的循環。這部作品讓我深刻體會到了人類存在的孤獨本質，以及對愛與理解的永恆渴望。"
    }
]

# 主標題
st.markdown("<h1 class='main-title'>我的閱讀筆記</h1>", unsafe_allow_html=True)

# 顯示書籍卡片
st.markdown("<div class='book-grid'>", unsafe_allow_html=True)

for book in books:
    st.markdown(f"""
    <div class="book-card">
        <img src="{book['cover']}" alt="{book['title']} 封面" class="book-cover">
        <div class="book-info">
            <h2 class="book-title">{book['title']}</h2>
            <p class="book-author">作者：{book['author']}</p>
            <p class="book-thoughts" id="thoughts-{book['id']}" style="display: none;">
                {book['thoughts']}
            </p>
            <span class="read-more" id="link-{book['id']}" onclick="toggleThoughts({book['id']})">閱讀更多</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 由於Streamlit的限制，我們需要一個小技巧來確保JavaScript能夠運行
st.markdown("""
<script>
    // 一個小技巧，確保腳本在每次重新渲染時都能執行
    document.addEventListener('DOMContentLoaded', (event) => {
        // 代碼已經在HTML中，所以這裡不需要額外的JavaScript
    });
</script>
""", unsafe_allow_html=True)
