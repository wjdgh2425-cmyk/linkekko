
from flask import Flask, render_template_string, Response
from datetime import datetime, timezone

app = Flask(__name__)

BASE_URL = "https://linkekko.onrender.com"

# =====================================
# 링크에코 사이트 목록
# =====================================

SITES = [
    # OTT · 동영상
    {"category": "OTT·동영상", "name": "티빙", "description": "드라마, 예능, 영화와 실시간 TV", "url": "https://www.tving.com/", "icon": "📺"},
    {"category": "OTT·동영상", "name": "넷플릭스", "description": "다양한 영화와 오리지널 시리즈", "url": "https://www.netflix.com/kr", "icon": "🎬"},
    {"category": "OTT·동영상", "name": "왓챠", "description": "영화와 드라마 감상 서비스", "url": "https://watcha.com/", "icon": "🍿"},
    {"category": "OTT·동영상", "name": "쿠팡플레이", "description": "영화, 드라마, 스포츠 콘텐츠", "url": "https://www.coupangplay.com/", "icon": "🎥"},
    {"category": "OTT·동영상", "name": "유튜브", "description": "다양한 영상과 크리에이터 콘텐츠", "url": "https://www.youtube.com/", "icon": "▶️"},
    {"category": "OTT·동영상", "name": "웨이브", "description": "방송 프로그램과 영화 감상", "url": "https://www.wavve.com/", "icon": "🌊"},
    {"category": "OTT·동영상", "name": "디즈니플러스", "description": "디즈니, 마블, 스타워즈 콘텐츠", "url": "https://www.disneyplus.com/ko-kr", "icon": "✨"},
    {"category": "OTT·동영상", "name": "라프텔", "description": "애니메이션 전문 스트리밍", "url": "https://laftel.net/", "icon": "🌸"},

    # 게임
    {"category": "게임", "name": "넥슨", "description": "다양한 온라인 게임과 게임 소식", "url": "https://www.nexon.com/", "icon": "🎮"},
    {"category": "게임", "name": "라이엇 게임즈", "description": "리그 오브 레전드와 라이엇 게임", "url": "https://www.riotgames.com/", "icon": "⚔️"},
    {"category": "게임", "name": "스팀", "description": "PC 게임 구매와 라이브러리", "url": "https://store.steampowered.com/", "icon": "🕹️"},
    {"category": "게임", "name": "플레이스테이션", "description": "플레이스테이션 게임과 콘솔 정보", "url": "https://www.playstation.com/ko-kr/", "icon": "🎯"},
    {"category": "게임", "name": "닌텐도", "description": "닌텐도 게임과 콘솔 정보", "url": "https://www.nintendo.com/kr/", "icon": "🍄"},
    {"category": "게임", "name": "배틀그라운드", "description": "배틀그라운드 공식 홈페이지", "url": "https://pubg.com/ko-kr", "icon": "🔫"},

    # 실시간 방송
    {"category": "실시간 방송", "name": "SOOP", "description": "실시간 방송과 스트리머 콘텐츠", "url": "https://www.sooplive.co.kr/", "icon": "📡"},
    {"category": "실시간 방송", "name": "치지직", "description": "게임과 다양한 실시간 방송", "url": "https://chzzk.naver.com/", "icon": "🟢"},
    {"category": "실시간 방송", "name": "유튜브 라이브", "description": "유튜브 실시간 스트리밍", "url": "https://www.youtube.com/live", "icon": "🔴"},
    {"category": "실시간 방송", "name": "틱톡", "description": "숏폼 영상과 라이브 방송", "url": "https://www.tiktok.com/", "icon": "🎵"},
    {"category": "실시간 방송", "name": "킥", "description": "글로벌 실시간 스트리밍 플랫폼", "url": "https://kick.com/", "icon": "💚"},

    # 만화 · 웹툰
    {"category": "만화·웹툰", "name": "네이버웹툰", "description": "다양한 장르의 인기 웹툰", "url": "https://comic.naver.com/", "icon": "📗"},
    {"category": "만화·웹툰", "name": "카카오웹툰", "description": "인기 웹툰과 독점 연재 작품", "url": "https://webtoon.kakao.com/", "icon": "📙"},
    {"category": "만화·웹툰", "name": "카카오페이지", "description": "웹툰과 웹소설 콘텐츠", "url": "https://page.kakao.com/", "icon": "📚"},
    {"category": "만화·웹툰", "name": "네이버 시리즈", "description": "웹툰과 웹소설 감상", "url": "https://series.naver.com/", "icon": "📖"},
    {"category": "만화·웹툰", "name": "레진코믹스", "description": "다양한 장르의 웹툰 플랫폼", "url": "https://www.lezhin.com/", "icon": "🎨"},
    {"category": "만화·웹툰", "name": "봄툰", "description": "다양한 장르의 웹툰 플랫폼", "url": "https://www.bomtoon.com/", "icon": "🌷"},
    {"category": "만화·웹툰", "name": "리디", "description": "웹툰, 웹소설과 전자책", "url": "https://ridibooks.com/", "icon": "📕"},
    {"category": "만화·웹툰", "name": "미스터블루", "description": "만화와 웹툰 콘텐츠", "url": "https://www.mrblue.com/", "icon": "🖌️"},
]

CATEGORIES = [
    "전체",
    "OTT·동영상",
    "게임",
    "실시간 방송",
    "만화·웹툰"
]

# =====================================
# 홈페이지
# =====================================

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>링크에코 | 분야별 공식 사이트 주소모아</title>

<meta name="description" content="링크에코는 OTT·동영상, 게임, 실시간 방송, 만화·웹툰 분야의 공식 사이트 주소를 한곳에 모아 편리하게 확인할 수 있는 주소모아 서비스입니다.">
<meta name="keywords" content="링크에코, 주소모아, 공식사이트, OTT, 게임, 실시간방송, 만화, 웹툰">
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="pPTsfFdNbqdZlwp9cF4Bp_mVbMWP-YJ_HMiEBsNr7B4">

<link rel="canonical" href="https://linkekko.onrender.com/">

<meta property="og:type" content="website">
<meta property="og:title" content="링크에코 | 분야별 공식 사이트 주소모아">
<meta property="og:description" content="자주 찾는 공식 사이트를 링크에코에서 한눈에 확인하세요.">
<meta property="og:url" content="https://linkekko.onrender.com/">
<meta property="og:site_name" content="링크에코">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "링크에코",
  "url": "https://linkekko.onrender.com/",
  "description": "분야별 공식 사이트 주소를 모아 제공하는 주소모아 서비스"
}
</script>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Pretendard', 'Noto Sans KR', Arial, sans-serif;
    background:
        radial-gradient(circle at 15% 10%, rgba(94, 48, 180, 0.23), transparent 35%),
        radial-gradient(circle at 85% 20%, rgba(0, 145, 255, 0.16), transparent 35%),
        #080b18;
    color: #fff;
    min-height: 100vh;
}

a {
    color: inherit;
    text-decoration: none;
}

header {
    width: 100%;
    padding: 22px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    background: rgba(8, 11, 24, 0.75);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 10;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    color: transparent;
}

.header-contact {
    font-size: 13px;
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.4);
    padding: 9px 15px;
    border-radius: 20px;
    transition: 0.2s;
}

.header-contact:hover {
    background: rgba(139,92,246,0.2);
}

/* 에코 메인 배경 사진 */

.hero {
    text-align: center;
    padding: 100px 20px 55px;
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(
            90deg,
            rgba(8, 11, 24, 0.96) 0%,
            rgba(8, 11, 24, 0.78) 48%,
            rgba(8, 11, 24, 0.25) 100%
        ),
        url("https://skins.nerfplz.com/art/245019_splash.jpg");
    background-size: cover;
    background-position: center 25%;
    background-repeat: no-repeat;
    min-height: 440px;
}

.hero::before {
    content: "";
    position: absolute;
    width: 340px;
    height: 340px;
    background: rgba(124,58,237,0.15);
    filter: blur(100px);
    border-radius: 50%;
    top: 0;
    left: calc(50% - 170px);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-label {
    display: inline-block;
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.35);
    background: rgba(124,58,237,0.12);
    border-radius: 30px;
    padding: 8px 16px;
    font-size: 12px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: clamp(36px, 6vw, 62px);
    margin: 0 0 18px;
    font-weight: 900;
    letter-spacing: -2px;
}

.hero h1 span {
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    color: transparent;
}

.hero p {
    color: #d0d5e5;
    line-height: 1.8;
    font-size: 15px;
    margin: 0 auto 30px;
}

.search-box {
    max-width: 580px;
    margin: 0 auto;
    display: flex;
    background: #151a2d;
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 15px;
    padding: 7px;
    box-shadow: 0 0 35px rgba(99,102,241,0.12);
}

.search-box input {
    flex: 1;
    min-width: 0;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    padding: 13px 15px;
    font-size: 14px;
}

.search-box input::placeholder {
    color: #a0a8bd;
}

.search-box button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    padding: 0 22px;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
}

.container {
    max-width: 1150px;
    margin: 0 auto;
    padding: 20px 22px 70px;
}

.category-list {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 15px 0 40px;
}

.category-btn {
    background: #151a2d;
    border: 1px solid #292f48;
    color: #aab3cc;
    padding: 11px 18px;
    border-radius: 30px;
    cursor: pointer;
    font-size: 13px;
    transition: 0.2s;
}

.category-btn:hover,
.category-btn.active {
    color: white;
    background: linear-gradient(135deg, #6d28d9, #2563eb);
    border-color: transparent;
}

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    gap: 10px;
}

.section-heading h2 {
    font-size: 21px;
    margin: 0;
}

.result-count {
    color: #858da8;
    font-size: 12px;
}

.site-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}

.site-card {
    background: linear-gradient(145deg, #171d32, #101527);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 17px;
    padding: 21px;
    min-height: 165px;
    position: relative;
    transition: 0.25s;
    display: flex;
    flex-direction: column;
}

.site-card:hover {
    transform: translateY(-5px);
    border-color: rgba(139,92,246,0.6);
    box-shadow: 0 10px 35px rgba(76,29,149,0.18);
}

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.site-icon {
    font-size: 26px;
}

.favorite {
    border: none;
    background: transparent;
    color: #67708a;
    font-size: 21px;
    cursor: pointer;
    padding: 0;
}

.favorite.active {
    color: #fbbf24;
}

.site-card h3 {
    margin: 0 0 8px;
    font-size: 17px;
}

.site-card p {
    color: #929bb4;
    font-size: 12px;
    line-height: 1.6;
    margin: 0 0 17px;
    flex: 1;
}

.visit-link {
    color: #a5b4fc;
    font-size: 12px;
    font-weight: bold;
}

.empty {
    display: none;
    text-align: center;
    color: #929bb4;
    padding: 45px 10px;
    background: #11172a;
    border-radius: 15px;
}

.info-section {
    margin-top: 65px;
    padding: 27px;
    border-radius: 17px;
    background: rgba(21,26,45,0.7);
    border: 1px solid rgba(148,163,184,0.12);
}

.info-section h2 {
    font-size: 19px;
    margin-top: 0;
}

.info-section p {
    color: #a5acc2;
    font-size: 13px;
    line-height: 1.9;
    margin-bottom: 0;
}

footer {
    border-top: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    padding: 30px 15px;
    color: #737d98;
    font-size: 12px;
    line-height: 2;
}

footer a {
    color: #a78bfa;
}

@media (max-width: 600px) {
    header {
        padding: 17px 5%;
    }

    .logo {
        font-size: 21px;
    }

    .hero {
        padding-top: 65px;
        min-height: 400px;
        background-position: 60% center;
    }

    .site-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .site-card {
        padding: 15px;
        min-height: 160px;
    }

    .site-card h3 {
        font-size: 15px;
    }

    .site-card p {
        font-size: 11px;
    }

    .category-btn {
        padding: 9px 13px;
        font-size: 12px;
    }
}
</style>
</head>

<body>

<header>
    <a class="logo" href="/">링크에코</a>

    <a class="header-contact"
       href="https://t.me/linkekko369"
       target="_blank"
       rel="noopener noreferrer">
        광고 문의
    </a>
</header>

<section class="hero">
    <div class="hero-content">

        <div class="hero-label">링크에코 · 주소모아</div>

        <h1>원하는 사이트를 <span>한곳에서</span></h1>

        <p>
            자주 찾는 공식 사이트를 분야별로 모았습니다.<br>
            링크에코에서 쉽고 빠르게 찾아보세요.
        </p>

        <div class="search-box">
            <input
                type="text"
                id="searchInput"
                placeholder="사이트 이름이나 키워드를 검색하세요"
                aria-label="사이트 검색"
            >

            <button onclick="searchSites()">검색</button>
        </div>

    </div>
</section>

<main class="container">

    <nav class="category-list" aria-label="사이트 카테고리">

        {% for category in categories %}
        <button
            class="category-btn {% if loop.first %}active{% endif %}"
            onclick="filterCategory('{{ category }}', this)"
        >
            {{ category }}
        </button>
        {% endfor %}

        <button class="category-btn" onclick="showFavorites(this)">
            ⭐ 즐겨찾기
        </button>

    </nav>

    <div class="section-heading">
        <h2 id="sectionTitle">전체 사이트</h2>
        <span class="result-count" id="resultCount"></span>
    </div>

    <section class="site-grid" id="siteGrid">

        {% for site in sites %}
        <article
            class="site-card"
            data-category="{{ site.category }}"
            data-name="{{ site.name }}"
            data-description="{{ site.description }}"
        >

            <div class="card-top">
                <span class="site-icon">{{ site.icon }}</span>

                <button
                    class="favorite"
                    aria-label="{{ site.name }} 즐겨찾기"
                    onclick="toggleFavorite('{{ site.name }}', this)"
                >☆</button>
            </div>

            <h3>{{ site.name }}</h3>

            <p>{{ site.description }}</p>

            <a
                class="visit-link"
                href="{{ site.url }}"
                target="_blank"
                rel="noopener noreferrer"
            >
                공식 사이트 방문 →
            </a>

        </article>
        {% endfor %}

    </section>

    <div class="empty" id="emptyMessage">
        검색 결과가 없습니다.
    </div>

    <section class="info-section">
        <h2>링크에코 주소모아 소개</h2>

        <p>
            링크에코는 다양한 분야의 공식 웹사이트 주소를 한곳에 모아
            편리하게 확인할 수 있도록 만든 주소모아 서비스입니다.
            OTT·동영상, 게임, 실시간 방송, 만화·웹툰 카테고리에서
            원하는 사이트를 쉽게 찾아볼 수 있습니다.
            검색 기능과 즐겨찾기를 이용해 자주 방문하는 사이트를
            더욱 편리하게 관리할 수 있습니다.
            링크에코는 각 서비스의 공식 홈페이지로 연결되는 링크를 제공합니다.
        </p>
    </section>

</main>

<footer>
    <div>© 2026 링크에코. 모든 권리 보유.</div>

    <div>
        사이트 관련 문의 및 광고 문의:
        <a
            href="https://t.me/linkekko369"
            target="_blank"
            rel="noopener noreferrer"
        >
            텔레그램 @linkekko369
        </a>
    </div>

    <div>링크에코는 각 외부 사이트와 별개의 서비스입니다.</div>
</footer>

<script>
let currentCategory = "전체";
let favoritesOnly = false;

function getCards() {
    return Array.from(document.querySelectorAll(".site-card"));
}

function updateCount(count) {
    document.getElementById("resultCount").textContent =
        "검색 결과 " + count + "개";
}

function applyFilters() {
    const keyword = document.getElementById("searchInput")
        .value.trim().toLowerCase();

    let visibleCount = 0;

    getCards().forEach(card => {
        const category = card.dataset.category;
        const name = card.dataset.name.toLowerCase();
        const description = card.dataset.description.toLowerCase();

        const categoryMatch =
            currentCategory === "전체" ||
            category === currentCategory;

        const keywordMatch =
            name.includes(keyword) ||
            description.includes(keyword) ||
            category.toLowerCase().includes(keyword);

        const favoriteMatch =
            !favoritesOnly || isFavorite(card.dataset.name);

        const visible =
            categoryMatch && keywordMatch && favoriteMatch;

        card.style.display = visible ? "flex" : "none";

        if (visible) visibleCount++;
    });

    updateCount(visibleCount);

    document.getElementById("emptyMessage").style.display =
        visibleCount === 0 ? "block" : "none";
}

function filterCategory(category, button) {
    currentCategory = category;
    favoritesOnly = false;

    document.querySelectorAll(".category-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    button.classList.add("active");

    document.getElementById("sectionTitle").textContent =
        category === "전체" ? "전체 사이트" : category;

    applyFilters();
}

function showFavorites(button) {
    currentCategory = "전체";
    favoritesOnly = true;

    document.querySelectorAll(".category-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    button.classList.add("active");

    document.getElementById("sectionTitle").textContent =
        "즐겨찾기 사이트";

    applyFilters();
}

function searchSites() {
    applyFilters();
}

document.getElementById("searchInput").addEventListener(
    "input",
    applyFilters
);

function getFavorites() {
    try {
        return JSON.parse(
            localStorage.getItem("linkekkoFavorites") || "[]"
        );
    } catch (error) {
        return [];
    }
}

function isFavorite(name) {
    return getFavorites().includes(name);
}

function toggleFavorite(name, button) {
    let favorites = getFavorites();

    if (favorites.includes(name)) {
        favorites = favorites.filter(item => item !== name);
    } else {
        favorites.push(name);
    }

    localStorage.setItem(
        "linkekkoFavorites",
        JSON.stringify(favorites)
    );

    updateFavoriteButtons();
    applyFilters();
}

function updateFavoriteButtons() {
    getCards().forEach(card => {
        const button = card.querySelector(".favorite");
        const active = isFavorite(card.dataset.name);

        button.textContent = active ? "★" : "☆";
        button.classList.toggle("active", active);
    });
}

updateFavoriteButtons();
applyFilters();
</script>

</body>
</html>
"""

# =====================================
# 홈페이지
# =====================================

@app.route("/")
def home():
    return render_template_string(
        HTML,
        sites=SITES,
        categories=CATEGORIES
    )


# =====================================
# 사이트맵
# =====================================

@app.route("/sitemap.xml")
def sitemap():
    today = datetime.now(timezone.utc).date().isoformat()

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{BASE_URL}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""

    return Response(xml, mimetype="application/xml")


# =====================================
# robots.txt
# =====================================

@app.route("/robots.txt")
def robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


# =====================================
# 서버 실행
# =====================================

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
