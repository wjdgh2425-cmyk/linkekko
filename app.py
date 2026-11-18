
from flask import Flask, render_template_string

app = Flask(__name__)

SITES = [
    {"category": "공공기관", "name": "정부24", "description": "민원 신청과 정부 서비스", "url": "https://www.gov.kr"},
    {"category": "공공기관", "name": "국세청", "description": "세금 신고와 국세 관련 서비스", "url": "https://www.nts.go.kr"},
    {"category": "공공기관", "name": "국민건강보험", "description": "건강보험 정보와 민원 서비스", "url": "https://www.nhis.or.kr"},
    {"category": "교육", "name": "한국장학재단", "description": "국가장학금과 학자금 지원", "url": "https://www.kosaf.go.kr"},
    {"category": "취업", "name": "고용24", "description": "일자리 검색과 고용 서비스", "url": "https://www.work24.go.kr"},
    {"category": "창업", "name": "K-스타트업", "description": "창업 지원 사업과 창업 정보", "url": "https://www.k-startup.go.kr"},
]

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LINK EKKO | 주소모아</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    background: #070b1c;
    color: #f5f8ff;
    font-family: Arial, sans-serif;
}

header {
    height: 75px;
    padding: 0 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #090e20;
    border-bottom: 1px solid #174d70;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 1px;
}

.logo span { color: #00e5ff; }

nav a {
    color: #dce8ff;
    text-decoration: none;
    margin-left: 22px;
    font-size: 14px;
}

.hero {
    min-height: 540px;
    padding: 65px 7% 35px;
    position: relative;
    overflow: hidden;
    background:
      linear-gradient(90deg, rgba(5,9,27,.98) 0%,
      rgba(5,9,27,.85) 43%, rgba(5,9,27,.2) 100%),
      url("https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ekko_7.jpg");
    background-size: cover;
    background-position: center 25%;
}

.hero-content {
    max-width: 650px;
    position: relative;
    z-index: 1;
}

.tag {
    color: #00e5ff;
    letter-spacing: 4px;
    font-weight: bold;
}

.hero h1 {
    font-size: clamp(48px, 8vw, 88px);
    line-height: 1;
    margin: 20px 0;
    font-style: italic;
    font-weight: 900;
}

.hero h1 span { color: #00d9ff; }

.hero p {
    color: #d0d9f5;
    font-size: 19px;
}

.search-box {
    display: flex;
    margin-top: 35px;
    max-width: 650px;
    border: 2px solid #00dfff;
    border-radius: 15px;
    overflow: hidden;
    background: #111a35;
    box-shadow: 0 0 22px #00cfff44;
}

.search-box input {
    flex: 1;
    min-width: 0;
    padding: 18px;
    border: none;
    outline: none;
    background: transparent;
    color: white;
    font-size: 16px;
}

.search-box button {
    border: none;
    padding: 0 27px;
    color: #001321;
    background: #00dfff;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
}

main {
    max-width: 1400px;
    margin: auto;
    padding: 25px 30px 60px;
}

.categories {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 10px 0 30px;
}

.categories button {
    padding: 12px 22px;
    border: 1px solid #29476b;
    border-radius: 30px;
    color: #dbeaff;
    background: #101831;
    cursor: pointer;
    font-size: 15px;
}

.categories button:hover,
.categories button.active {
    color: #001321;
    background: #00dfff;
    border-color: #00dfff;
    box-shadow: 0 0 18px #00dfff66;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
}

.site {
    padding: 23px;
    border: 1px solid #27618b;
    border-radius: 18px;
    background: linear-gradient(145deg, #17284b, #101329);
    box-shadow: 0 8px 25px #0008;
    transition: .2s;
}

.site:hover {
    transform: translateY(-5px);
    border-color: #00e5ff;
    box-shadow: 0 0 22px #00dfff33;
}

.site small {
    color: #00e5ff;
    font-weight: bold;
}

.site h2 {
    font-size: 23px;
    margin: 18px 0 8px;
}

.site p {
    color: #b9c8e8;
    min-height: 42px;
    line-height: 1.5;
}

.site-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 20px;
}

.site a {
    display: inline-block;
    padding: 11px 14px;
    border-radius: 9px;
    background: #124bd8;
    color: white;
    text-decoration: none;
    font-weight: bold;
    font-size: 13px;
}

.favorite {
    border: 1px solid #47658c;
    border-radius: 9px;
    padding: 9px 12px;
    background: #172442;
    color: #fff;
    cursor: pointer;
}

.favorite.saved { color: #ffdc55; }

#empty {
    display: none;
    text-align: center;
    padding: 40px;
    color: #b9c8e8;
}

footer {
    padding: 30px;
    text-align: center;
    color: #a9badc;
    border-top: 1px solid #174d70;
}

footer span { color: #00dfff; }

@media (max-width: 650px) {
    header { padding: 0 18px; }
    nav a { margin-left: 8px; font-size: 12px; }
    .hero { padding: 55px 22px; }
    .hero p { font-size: 16px; }
    main { padding: 20px 16px 40px; }
}
</style>
</head>

<body>

<header>
    <div class="logo">⌛ LINK <span>EKKO</span> | 주소모아</div>
    <nav>
        <a href="/">홈</a>
        <a href="#categories">카테고리</a>
        <a href="#sites">사이트</a>
    </nav>
</header>

<section class="hero">
    <div class="hero-content">
        <div class="tag">TRUE DAMAGE · LINK EKKO</div>
        <h1>LINK <span>EKKO</span></h1>
        <h2>필요한 공식 사이트를 한곳에, 주소모아!</h2>
        <p>분야별 검증된 공식 사이트를 쉽고 빠르게 찾아보세요.</p>

        <div class="search-box">
            <input id="search" type="text"
                placeholder="사이트 이름이나 분야를 검색하세요..."
                oninput="filterSites()">
            <button onclick="filterSites()">검색</button>
        </div>
    </div>
</section>

<main>
    <div class="categories" id="categories">
        <button class="active" onclick="chooseCategory('전체', this)">전체</button>
        <button onclick="chooseCategory('공공기관', this)">공공기관</button>
        <button onclick="chooseCategory('교육', this)">교육</button>
        <button onclick="chooseCategory('취업', this)">취업</button>
        <button onclick="chooseCategory('창업', this)">창업</button>
        <button onclick="chooseCategory('즐겨찾기', this)">★ 즐겨찾기</button>
    </div>

    <section class="grid" id="sites">
        {% for site in sites %}
        <article class="site"
            data-category="{{ site.category }}"
            data-search="{{ site.name }} {{ site.category }} {{ site.description }}"
            data-url="{{ site.url }}">

            <small>{{ site.category }}</small>
            <h2>{{ site.name }}</h2>
            <p>{{ site.description }}</p>

            <div class="site-actions">
                <a href="{{ site.url }}" target="_blank"
                   rel="noopener noreferrer">공식 사이트 방문하기 ↗</a>
                <button class="favorite" onclick="toggleFavorite(this)"
                    aria-label="즐겨찾기">☆</button>
            </div>
        </article>
        {% endfor %}
    </section>

    <div id="empty">검색 결과가 없습니다.</div>
</main>

<footer>
    <h2>⌛ LINK <span>EKKO</span> · 주소모아</h2>
    더 나은 인터넷 생활을 위한 공식 사이트 모음 서비스
    <p>Find it. Link it. LINK EKKO!</p>
</footer>

<script>
let selectedCategory = "전체";

function getFavorites() {
    try {
        return JSON.parse(localStorage.getItem("linkekko_favorites") || "[]");
    } catch (e) {
        return [];
    }
}

function toggleFavorite(button) {
    const card = button.closest(".site");
    const url = card.dataset.url;
    let favorites = getFavorites();

    if (favorites.includes(url)) {
        favorites = favorites.filter(item => item !== url);
    } else {
        favorites.push(url);
    }

    localStorage.setItem("linkekko_favorites", JSON.stringify(favorites));
    updateFavorites();
    filterSites();
}

function updateFavorites() {
    const favorites = getFavorites();

    document.querySelectorAll(".site").forEach(card => {
        const button = card.querySelector(".favorite");
        const saved = favorites.includes(card.dataset.url);
        button.classList.toggle("saved", saved);
        button.textContent = saved ? "★" : "☆";
    });
}

function chooseCategory(category, button) {
    selectedCategory = category;

    document.querySelectorAll(".categories button").forEach(item => {
        item.classList.remove("active");
    });

    button.classList.add("active");
    filterSites();
}

function filterSites() {
    const keyword = document.getElementById("search").value.toLowerCase();
    const favorites = getFavorites();
    let count = 0;

    document.querySelectorAll(".site").forEach(card => {
        const category = card.dataset.category;
        const content = card.dataset.search.toLowerCase();
        const isFavorite = favorites.includes(card.dataset.url);

        const categoryMatch =
            selectedCategory === "전체" ||
            category === selectedCategory ||
            (selectedCategory === "즐겨찾기" && isFavorite);

        const keywordMatch = content.includes(keyword);
        const visible = categoryMatch && keywordMatch;

        card.style.display = visible ? "block" : "none";
        if (visible) count++;
    });

    document.getElementById("empty").style.display =
        count === 0 ? "block" : "none";
}

updateFavorites();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, sites=SITES)

if __name__ == "__main__":
    app.run(debug=True)
