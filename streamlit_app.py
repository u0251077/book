import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 設置頁面配置
st.set_page_config(page_title="我的閱讀筆記", layout="wide")

# 自定義CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');
    
    .stApp {
        font-family: 'Noto Sans TC', sans-serif;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .book-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5em;
        margin-bottom: 2em;
    }
    .book-title {
        color: #34495e;
        font-size: 1.8em;
        margin-bottom: 0.5em;
    }
    .book-author {
        color: #7f8c8d;
        font-style: italic;
        margin-bottom: 1em;
    }
    .book-cover {
        width: 100%;
        max-width: 300px;
        height: auto;
        border-radius: 5px;
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

# 輔助函數：獲取圖片
def get_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# 書籍數據
books = [
    {
        "id": 1,
        "title": "哈利波特與魔法石",
        "author": "J.K. 羅琳",
        "cover": "https://via.placeholder.com/300x450.png?text=哈利波特與魔法石",
        "thoughts": "這本書開啟了一個魔法世界的大門，讓我感受到了想像力的無窮魅力。哈利波特的冒險不僅僅是一個男孩的成長故事，更是關於友誼、勇氣和選擇的深刻寓言。羅琳筆下的霍格華茲魔法學校充滿了奇思妙想，每個角色都栩栩如生。這本書教會了我，即使在最黑暗的時刻，只要有希望和勇氣，我們也能找到光明。"
    },
    {
        "id": 2,
        "title": "三體",
        "author": "劉慈欣",
        "cover": "https://via.placeholder.com/300x450.png?text=三體",
        "thoughts": "《三體》是一部震撼人心的科幻巨作，它不僅展現了宏大的宇宙觀，還深入探討了人性的複雜性。劉慈欣以獨特的視角審視人類文明的脆弱性和宇宙文明間的殘酷競爭。書中對科技發展、哲學思考和人類命運的描述令人深思。通過地球文明面對外星威脅的故事，我更深刻地理解了人類在宇宙中的渺小，同時也感受到了人類意志的偉大。"
    },
    {
        "id": 3,
        "title": "百年孤獨",
        "author": "加布里埃爾·加西亞·馬爾克斯",
        "cover": "https://via.placeholder.com/300x450.png?text=百年孤獨",
        "thoughts": "馬爾克斯的《百年孤獨》是一部魔幻現實主義的經典之作。通過布恩迪亞家族七代人的故事，書中呈現了拉丁美洲的歷史縮影和人性的複雜面貌。這本書的敘事方式獨特，將現實與幻想、個人命運與歷史進程巧妙地交織在一起。閱讀過程中，我彷彿置身於馬孔多這個虛構小鎮，感受到了時間的流逝和命運的循環。這部作品讓我深刻體會到了人類存在的孤獨本質，以及對愛與理解的永恆渴望。"
    }
]

# 主標題
st.title("我的閱讀筆記")

# 顯示書籍卡片
for book in books:
    with st.container():
        st.markdown(f"<div class='book-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(get_image(book['cover']), caption=f"{book['title']} 封面", use_column_width=True)
        
        with col2:
            st.markdown(f"<h2 class='book-title'>{book['title']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p class='book-author'>作者：{book['author']}</p>", unsafe_allow_html=True)
            
            with st.expander("閱讀心得"):
                st.write(book['thoughts'])
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)  # 添加一些底部間距
