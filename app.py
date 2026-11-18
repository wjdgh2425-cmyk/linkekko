
from flask import Flask, render_template_string, Response

app = Flask(__name__)

# =====================================
# LINK EKKO 사이트 데이터
# =====================================

SITES = [
    {
        "category": "만화",
        "name": "마루마루",
        "description": "만화 관련 외부 사이트",
        "url": "https://marumaru111.com/"
    },
    {
        "category": "애니메이션",
        "name": "애니울프",
        "description": "애니메이션 관련 외부 사이트",
        "url": "https://aniwolf.com/"
    },
    {
        "category": "웹툰·만화",
        "name": "뚜툰",
        "description": "웹툰 및 만화 관련 외부 사이트",
        "url": "https://ufo1004.com/"
    },
    {
        "category": "성인·유흥정보",
        "name": "오피뷰",
        "description": "성인 대상 유흥업소 정보 사이트 · 만 19세 이상",
        "url": "https://opview88.com/"
    },
    {
        "category": "영화·드라마",
        "name": "티비혼",
        "description": "영화 및 드라마 관련 외부 사이트",
        "url": "https://tvhon11.com/"
    }
]

CATEGORIES = list(dict.fromkeys(
    site["category"] for site in SITES
))


# =====================================
# 홈페이지 HTML
# =====================================

HTML = """
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>LINK EKKO | 링크 에코 주소모아</title>

<meta name="description"
content="LINK EKKO(링크 에코 주소모아)는 만화, 애니메이션, 웹툰, 영화 등 다양한 분야의 외부 사이트 주소를 한곳에서 편리하게 찾아볼 수 있는 사이트 모음 서비스입니다.">

<meta name="keywords"
content="LINK EKKO, 링크 에코, 주소모아, 사이트모음, 사이트 주소">

<meta name="robots" content="index, follow">

<meta name="google-site-verification"
content="pPTsfFdNbqdZlwp9cF4Bp_mVbMWP-YJ_HMiEBsNr7B4" />

<meta property="og:title" content="LINK EKKO | 링크 에코 주소모아">
<meta property="og:description"
content="원하는 사이트를 한곳에, 주소모아! LINK EKKO에서 다양한 분야의 사이트를 찾아보세요.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://linkekko.onrender.com/">

<style>

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    background: #070b1c;
    color: #f5f8ff;
    font-family: Arial, sans-serif;
}

header {
    min-height: 70px;
    padding: 12px 5%;
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

.logo span {
    color: #00e5ff;
}

nav a {
    color: #dce8ff;
    text-decoration: none;
    margin-left: 22px;
    font-size: 14px;
}

nav a:hover {
    color: #00e5ff;
}

.hero {
    min-height: 570px;
    padding: 75px 7%;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;

    background:
        radial-gradient(
            circle at 80% 50%,
            #123b5c 0%,
            #10132c 35%,
            #070b1c 75%
        );
}

.ekko-art {
    position: absolute;
    right: 0;
    top: 0;
    width: 65%;
    height: 100%;
    object-fit: cover;
    object-position: center 25%;
    z-index: 0;
    opacity: 0.95;

    -webkit-mask-image:
        linear-gradient(to right, transparent 0%, black 38%);
    mask-image:
        linear-gradient(to right, transparent 0%, black 38%);
}

.image-error {
    display: none;
    position: absolute;
    right: 8%;
    bottom: 25px;
    z-index: 2;
    color: #9fb8d9;
    font-size: 12px;
}

.hero::after {
    content: "";
    position: absolute;
    inset: 0;

    background: linear-gradient(
        90deg,
        #070b1c 0%,
        rgba(7, 11, 28, 0.95) 34%,
        rgba(7, 11, 28, 0.15) 100%
    );

    z-index: 1;
    pointer-events: none;
}

.hero-content {
    max-width: 650px;
    position: relative;
    z-index: 2;
}

.tag {
    color: #00e5ff;
    letter-spacing: 4px;
    font-weight: bold;
    font-size: 15px;
}

.hero h1 {
    font-size: clamp(48px, 8vw, 88px);
    line-height: 1;
    margin: 22px 0;
    font-style: italic;
    font-weight: 900;
}

.hero h1 span {
    color: #00d9ff;
}

.hero h2 {
    font-size: 25px;
}

.hero p {
    color: #d0d9f5;
    font-size: 18px;
    line-height: 1.6;
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

.search-box button:hover {
    background: #69f0ff;
}

main {
    max-width: 1400px;
    margin: auto;
    padding: 35px 30px 70px;
}

.section-title {
    text-align: center;
    margin-bottom: 28px;
}

.section-title h2 {
    font-size: 28px;
}

.section-title p {
    color: #aebfdf;
}

.notice {
    max-width: 900px;
    margin: 0 auto 25px;
    padding: 15px 18px;
    border: 1px solid #6b5930;
    border-radius: 12px;
    background: #211d16;
    color: #f1d69b;
    font-size: 13px;
    line-height: 1.7;
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
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
}

.site {
    padding: 23px;
    border: 1px solid #27618b;
    border-radius: 18px;

    background: linear-gradient(
        145deg,
        #17284b,
        #101329
    );

    box-shadow: 0 8px 25px #0008;
    transition: 0.2s;
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

.site a:hover {
    background: #00bde9;
    color: #001321;
}

.favorite {
    border: 1px solid #47658c;
    border-radius: 9px;
    padding: 9px 12px;
    background: #172442;
    color: white;
    cursor: pointer;
    font-size: 17px;
}

.favorite.saved {
    color: #ffdc55;
}

#empty {
    display: none;
    text-align: center;
    padding: 40px;
    color: #b9c8e8;
}

footer {
    padding: 35px 20px;
    text-align: center;
    color: #a9badc;
    border-top: 1px solid #174d70;
    background: #090e20;
}

footer span {
    color: #00dfff;
}

@media (max-width: 700px) {

    header {
        padding: 15px 18px;
    }

    .logo {
        font-size: 19px;
    }

    nav a {
        margin-left: 8px;
        font-size: 12px;
    }

    .hero {
        min-height: 650px;
        padding: 55px 22px;
        align-items: flex-start;
    }

    .ekko-art {
        width: 100%;
        height: 65%;
        top: auto;
        bottom: 0;
        opacity: 0.7;

        -webkit-mask-image:
            linear-gradient(to bottom, transparent 0%, black 35%);
        mask-image:
            linear-gradient(to bottom, transparent 0%, black 35%);
    }

    .hero::after {
        background: linear-gradient(
            180deg,
            #070b1c 0%,
            rgba(7, 11, 28, 0.75) 48%,
            rgba(7, 11, 28, 0.1) 100%
        );
    }

    .hero h2 {
        font-size: 20px;
    }

    .hero p {
        font-size: 15px;
    }

    main {
        padding: 25px 16px 45px;
    }
}

</style>
</head>

<body>

<header>

    <div class="logo">
        ⌛ LINK <span>EKKO</span> | 주소모아
    </div>

    <nav>
        <a href="/">홈</a>
        <a href="#categories">카테고리</a>
        <a href="#sites">사이트</a>
    </nav>

</header>

<section class="hero">

    <img
        class="ekko-art"
        id="ekkoImage"
        src="https://skins.nerfplz.com/art/245019_splash.jpg"
        alt="리그 오브 레전드 트루 데미지 에코"

        onerror="
            if (!this.dataset.fallback) {
                this.dataset.fallback = '1';
                this.src =
                'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ekko_5.jpg';
            } else {
                this.style.display = 'none';
                document.getElementById('imageError').style.display = 'block';
            }
        "
    >

    <div class="image-error" id="imageError">
        에코 이미지를 불러오지 못했습니다.
    </div>

    <div class="hero-content">

        <div class="tag">
            TRUE DAMAGE · LINK EKKO
        </div>

        <h1>
            LINK <span>EKKO</span>
        </h1>

        <h2>
            원하는 사이트를 한곳에, 주소모아!
        </h2>

        <p>
            다양한 분야의 사이트를
            쉽고 빠르게 찾아보세요.
        </p>

        <div class="search-box">

            <input
                id="search"
                type="text"
                placeholder="사이트 이름이나 분야를 검색하세요..."
                oninput="filterSites()"
            >

            <button onclick="filterSites()">
                검색
            </button>

        </div>

    </div>

</section>

<main>

    <div class="section-title">

        <h2>사이트 모아보기</h2>

        <p>
            원하는 분야를 선택하고 사이트를 찾아보세요.
        </p>

    </div>

    <div class="notice">
        안내: 아래 사이트는 외부 사이트 링크 모음입니다.
        LINK EKKO가 해당 사이트의 운영 주체이거나 공식 제휴 관계임을 의미하지 않습니다.
        콘텐츠의 저작권 및 이용 권한은 별도로 확인해 주세요.
        성인 대상 사이트는 만 19세 이상만 이용할 수 있습니다.
    </div>

    <div class="categories" id="categories">

        <button
            class="active"
            onclick="chooseCategory('전체', this)"
        >
            전체
        </button>

        {% for category in categories %}

        <button
            onclick="chooseCategory('{{ category }}', this)"
        >
            {{ category }}
        </button>

        {% endfor %}

        <button
            onclick="chooseCategory('즐겨찾기', this)"
        >
            ★ 즐겨찾기
        </button>

    </div>

    <section class="grid" id="sites">

        {% for site in sites %}

        <article
            class="site"
            data-category="{{ site.category }}"
            data-search="{{ site.name }} {{ site.category }} {{ site.description }}"
            data-url="{{ site.url }}"
        >

            <small>
                {{ site.category }}
            </small>

            <h2>
                {{ site.name }}
            </h2>

            <p>
                {{ site.description }}
            </p>

            <div class="site-actions">

                <a
                    href="{{ site.url }}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    사이트 방문하기 ↗
                </a>

                <button
                    class="favorite"
                    onclick="toggleFavorite(this)"
                    aria-label="즐겨찾기"
                >
                    ☆
                </button>

            </div>

        </article>

        {% endfor %}

    </section>

    <div id="empty">
        검색 결과가 없습니다.
    </div>

</main>

<footer>

    <h2>
        ⌛ LINK <span>EKKO</span> · 주소모아
    </h2>

    다양한 사이트를 한곳에서 편리하게!

    <p>
        Find it. Link it. LINK EKKO!
    </p>

</footer>

<script>

let selectedCategory = "전체";

function getFavorites() {

    try {

        return JSON.parse(
            localStorage.getItem("linkekko_favorites") || "[]"
        );

    } catch (error) {

        return [];

    }

}

function toggleFavorite(button) {

    const card = button.closest(".site");
    const url = card.dataset.url;

    let favorites = getFavorites();

    if (favorites.includes(url)) {

        favorites = favorites.filter(
            item => item !== url
        );

    } else {

        favorites.push(url);

    }

    localStorage.setItem(
        "linkekko_favorites",
        JSON.stringify(favorites)
    );

    updateFavorites();
    filterSites();

}

function updateFavorites() {

    const favorites = getFavorites();

    document.querySelectorAll(".site").forEach(card => {

        const button = card.querySelector(".favorite");

        const saved = favorites.includes(
            card.dataset.url
        );

        button.classList.toggle("saved", saved);
        button.textContent = saved ? "★" : "☆";

    });

}

function chooseCategory(category, button) {

    selectedCategory = category;

    document.querySelectorAll(
        ".categories button"
    ).forEach(item => {

        item.classList.remove("active");

    });

    button.classList.add("active");

    filterSites();

}

function filterSites() {

    const keyword = document
        .getElementById("search")
        .value.toLowerCase();

    const favorites = getFavorites();

    let count = 0;

    document.querySelectorAll(".site").forEach(card => {

        const category = card.dataset.category;
        const content = card.dataset.search.toLowerCase();

        const isFavorite = favorites.includes(
            card.dataset.url
        );

        const categoryMatch =
            selectedCategory === "전체" ||
            category === selectedCategory ||
            (
                selectedCategory === "즐겨찾기"
                && isFavorite
            );

        const keywordMatch = content.includes(keyword);

        const visible = categoryMatch && keywordMatch;

        card.style.display = visible ? "block" : "none";

        if (visible) {
            count++;
        }

    });

    document.getElementById("empty").style.display =
        count === 0 ? "block" : "none";

}

updateFavorites();

</script>

</body>
</html>
"""


# =====================================
# 구글 사이트맵
# =====================================

@app.route("/sitemap.xml")
def sitemap():

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://linkekko.onrender.com/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""

    return Response(
        xml,
        mimetype="application/xml"
    )


# =====================================
# robots.txt
# =====================================

@app.route("/robots.txt")
def robots():

    content = """User-agent: *
Allow: /

Sitemap: https://linkekko.onrender.com/sitemap.xml
"""

    return Response(
        content,
        mimetype="text/plain"
    )


# =====================================
# 홈페이지 실행
# =====================================

@app.route("/")
def home():

    return render_template_string(
        HTML,
        sites=SITES,
        categories=CATEGORIES
    )


if __name__ == "__main__":
    app.run(debug=True)
