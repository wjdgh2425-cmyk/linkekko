
from flask import Flask, render_template_string, Response
from datetime import datetime, timezone

app = Flask(__name__)

BASE_URL = "https://linkekko.onrender.com"

# =====================================
# LINK EKKO 사이트 목록
# =====================================

SITES = [
    {
        "category": "OTT·동영상",
        "name": "티빙",
        "description": "드라마, 예능, 영화 등 다양한 콘텐츠를 감상하는 OTT 서비스",
        "url": "https://www.tving.com/",
        "icon": "📺",
        "tag": "K-콘텐츠"
    },
    {
        "category": "OTT·동영상",
        "name": "넷플릭스",
        "description": "영화, 드라마, 다큐멘터리 등 다양한 콘텐츠를 제공하는 글로벌 OTT 서비스",
        "url": "https://www.netflix.com/kr",
        "icon": "🎬",
        "tag": "글로벌 OTT"
    },
    {
        "category": "OTT·동영상",
        "name": "왓챠",
        "description": "영화와 드라마를 감상하고 취향에 맞는 작품을 발견하는 OTT 서비스",
        "url": "https://watcha.com/ko/browse/all",
        "icon": "🍿",
        "tag": "영화·드라마"
    },
    {
        "category": "OTT·동영상",
        "name": "쿠팡플레이",
        "description": "영화, 드라마, 예능 및 스포츠 콘텐츠를 감상하는 스트리밍 서비스",
        "url": "https://www.coupangplay.com/",
        "icon": "▶️",
        "tag": "스포츠·엔터"
    },
    {
        "category": "OTT·동영상",
        "name": "유튜브",
        "description": "영상, 음악, 라이브 방송 및 크리에이터 콘텐츠를 감상하는 동영상 플랫폼",
        "url": "https://www.youtube.com/",
        "icon": "▶",
        "tag": "동영상"
    }
]

CATEGORIES = list(dict.fromkeys(
    site["category"] for site in SITES
))

STRUCTURED_DATA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "LINK EKKO",
    "alternateName": "링크 에코 주소모아",
    "url": BASE_URL,
    "description": "분야별 사이트 주소를 모아 편리하게 찾아볼 수 있는 주소모아 서비스입니다.",
    "inLanguage": "ko-KR"
}

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
          content="LINK EKKO 주소모아에서 티빙, 넷플릭스, 왓챠, 쿠팡플레이, 유튜브 등 다양한 OTT·동영상 사이트를 확인하세요.">

    <meta name="keywords"
          content="LINK EKKO, 링크 에코, 주소모아, 티빙, 넷플릭스, 왓챠, 쿠팡플레이, 유튜브">

    <meta name="robots" content="index, follow">

    <meta name="google-site-verification"
          content="pPTsfFdNbqdZlwp9cF4Bp_mVbMWP-YJ_HMiEBsNr7B4">

    <link rel="canonical" href="https://linkekko.onrender.com/">

    <meta property="og:type" content="website">
    <meta property="og:title" content="LINK EKKO | 링크 에코 주소모아">
    <meta property="og:description"
          content="자주 찾는 사이트를 LINK EKKO에서 편리하게 확인하세요.">
    <meta property="og:url" content="https://linkekko.onrender.com/">

    <script type="application/ld+json">
        {{ structured_data | tojson }}
    </script>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, "Malgun Gothic", sans-serif;
            background: #080b18;
            color: #fff;
            min-height: 100vh;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .background-glow {
            position: fixed;
            inset: 0;
            z-index: -2;
            background:
                radial-gradient(circle at 15% 15%,
                    rgba(0,225,255,.14), transparent 32%),
                radial-gradient(circle at 85% 25%,
                    rgba(139,70,255,.17), transparent 35%),
                #080b18;
        }

        .background-grid {
            position: fixed;
            inset: 0;
            z-index: -1;
            opacity: .12;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(0,220,255,.12) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,220,255,.12) 1px, transparent 1px);
            background-size: 45px 45px;
        }

        header {
            padding: 23px 7%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,.08);
            background: rgba(8,11,24,.8);
        }

        .logo {
            font-size: 25px;
            font-weight: 900;
            letter-spacing: 2px;
            text-shadow: 0 0 15px rgba(0,220,255,.65);
        }

        .logo span {
            color: #00e5ff;
        }

        .header-label {
            color: #9ba9c8;
            font-size: 13px;
            letter-spacing: 1px;
        }

        .hero {
            max-width: 1250px;
            min-height: 340px;
            margin: 38px auto 25px;
            padding: 65px 55px;
            border: 1px solid rgba(0,220,255,.23);
            border-radius: 24px;
            background:
                linear-gradient(90deg,
                    rgba(7,10,25,.97),
                    rgba(7,10,25,.78),
                    rgba(7,10,25,.35)),
                url("https://skins.nerfplz.com/art/245019_splash.jpg")
                center 25% / cover no-repeat,
                #111a35;
            box-shadow: 0 15px 55px rgba(0,0,0,.35);
        }

        .hero-tag {
            display: inline-block;
            padding: 8px 13px;
            border: 1px solid rgba(0,225,255,.5);
            border-radius: 30px;
            color: #00e5ff;
            font-size: 12px;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        .hero h1 {
            font-size: clamp(34px,5vw,58px);
            line-height: 1.15;
            margin-bottom: 18px;
        }

        .hero h1 span {
            color: #00e5ff;
            text-shadow: 0 0 22px rgba(0,225,255,.45);
        }

        .hero p {
            color: #c0cbe0;
            font-size: 16px;
            line-height: 1.8;
        }

        .container {
            max-width: 1250px;
            margin: 0 auto;
            padding: 20px 20px 70px;
        }

        .section-heading {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 35px 0 20px;
            gap: 15px;
        }

        .section-heading h2 {
            font-size: 24px;
        }

        .section-heading h2 span {
            color: #00e5ff;
        }

        .site-count {
            color: #8e9bb8;
            font-size: 13px;
        }

        .search-box {
            width: 100%;
            padding: 19px 22px;
            margin: 20px 0;
            border-radius: 14px;
            border: 1px solid rgba(0,225,255,.25);
            outline: none;
            color: white;
            background: rgba(17,25,48,.9);
            font-size: 15px;
        }

        .search-box:focus {
            border-color: #00e5ff;
            box-shadow: 0 0 18px rgba(0,225,255,.15);
        }

        .search-box::placeholder {
            color: #7e8ba8;
        }

        .filter-area {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 10px 0 28px;
        }

        .filter-btn {
            border: 1px solid rgba(255,255,255,.12);
            background: #161e36;
            color: #b8c4dc;
            border-radius: 30px;
            padding: 10px 17px;
            cursor: pointer;
            font-size: 13px;
        }

        .filter-btn:hover,
        .filter-btn.active {
            color: #07101e;
            background: #00e5ff;
            border-color: #00e5ff;
        }

        .site-grid {
            display: grid;
            grid-template-columns: repeat(3,minmax(0,1fr));
            gap: 18px;
        }

        .site-card {
            position: relative;
            min-height: 190px;
            padding: 24px;
            border-radius: 17px;
            border: 1px solid rgba(255,255,255,.09);
            background: linear-gradient(145deg,#17223e,#0c1224);
            transition: .25s;
            display: flex;
            flex-direction: column;
        }

        .site-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0,225,255,.55);
            box-shadow: 0 12px 30px rgba(0,180,255,.10);
        }

        .card-top {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 17px;
        }

        .site-icon {
            width: 48px;
            height: 48px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 13px;
            background: rgba(0,225,255,.10);
            font-size: 23px;
        }

        .site-name {
            font-size: 19px;
            font-weight: 800;
        }

        .site-category {
            color: #00dff5;
            font-size: 11px;
            margin-top: 5px;
        }

        .site-description {
            color: #9eacc8;
            font-size: 13px;
            line-height: 1.7;
            flex: 1;
            margin-bottom: 17px;
        }

        .card-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .site-tag {
            color: #aab8d2;
            font-size: 11px;
            padding: 6px 9px;
            border-radius: 20px;
            background: rgba(255,255,255,.06);
        }

        .visit-btn {
            color: #06101d;
            background: #00e5ff;
            padding: 9px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 800;
        }

        .visit-btn:hover {
            background: white;
        }

        .favorite-btn {
            position: absolute;
            top: 18px;
            right: 18px;
            border: 0;
            background: transparent;
            color: #7e8ba8;
            font-size: 21px;
            cursor: pointer;
        }

        .favorite-btn.active {
            color: #ff4f91;
        }

        .empty-message {
            display: none;
            padding: 45px 15px;
            color: #9eacc8;
            text-align: center;
            border: 1px dashed rgba(255,255,255,.15);
            border-radius: 15px;
        }

        .intro {
            margin-top: 55px;
            padding: 25px;
            border-left: 3px solid #00e5ff;
            background: rgba(14,24,46,.65);
            border-radius: 0 12px 12px 0;
        }

        .intro h2 {
            font-size: 18px;
            margin-bottom: 12px;
        }

        .intro p {
            color: #9eacc8;
            font-size: 13px;
            line-height: 1.9;
        }

        /* 광고문의 영역 */

        .contact-section {
            max-width: 650px;
            margin: 45px auto 0;
            padding: 30px 25px;
            text-align: center;
            border: 1px solid rgba(0,225,255,.28);
            border-radius: 18px;
            background: linear-gradient(
                145deg,
                rgba(20,35,65,.95),
                rgba(10,17,35,.95)
            );
            box-shadow: 0 10px 35px rgba(0,0,0,.2);
        }

        .contact-section h2 {
            font-size: 22px;
            margin-bottom: 10px;
        }

        .contact-section h2 span {
            color: #00e5ff;
        }

        .contact-section p {
            color: #9eacc8;
            font-size: 14px;
            line-height: 1.8;
            margin-bottom: 20px;
        }

        .telegram-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 13px 23px;
            border-radius: 30px;
            background: #229ED9;
            color: white;
            font-size: 14px;
            font-weight: 800;
            transition: .2s;
        }

        .telegram-btn:hover {
            background: #168ac2;
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(34,158,217,.25);
        }

        .telegram-icon {
            font-size: 19px;
        }

        .telegram-id {
            display: block;
            margin-top: 13px;
            color: #00e5ff;
            font-size: 13px;
        }

        footer {
            border-top: 1px solid rgba(255,255,255,.08);
            padding: 28px 20px;
            text-align: center;
            color: #71809e;
            font-size: 12px;
            line-height: 1.9;
        }

        footer strong {
            color: #00dff5;
            letter-spacing: 1px;
        }

        @media (max-width: 900px) {
            .site-grid {
                grid-template-columns: repeat(2,minmax(0,1fr));
            }

            .hero {
                margin: 25px 15px;
            }
        }

        @media (max-width: 600px) {
            header {
                padding: 18px 5%;
            }

            .logo {
                font-size: 21px;
            }

            .header-label {
                font-size: 10px;
            }

            .hero {
                min-height: 300px;
                padding: 48px 25px;
                background-position: 58% center;
            }

            .hero p {
                font-size: 14px;
            }

            .container {
                padding: 10px 15px 50px;
            }

            .site-grid {
                grid-template-columns: 1fr;
            }

            .section-heading h2 {
                font-size: 20px;
            }
        }
    </style>
</head>

<body>
    <div class="background-glow"></div>
    <div class="background-grid"></div>

    <header>
        <a class="logo" href="/">LINK <span>EKKO</span></a>
        <div class="header-label">LINK COLLECTION SERVICE</div>
    </header>

    <section class="hero">
        <div class="hero-tag">WELCOME TO LINK EKKO</div>
        <h1>YOUR LINK<br><span>YOUR WORLD.</span></h1>
        <p>
            자주 찾는 사이트를 한곳에서.<br>
            LINK EKKO에서 원하는 사이트를 쉽고 빠르게 찾아보세요.
        </p>
    </section>

    <main class="container">
        <div class="section-heading">
            <h2>EXPLORE <span>LINKS</span></h2>
            <div class="site-count">등록된 사이트 {{ sites|length }}개</div>
        </div>

        <input
            id="searchInput"
            class="search-box"
            type="search"
            placeholder="사이트 이름이나 설명을 검색하세요..."
            aria-label="사이트 검색"
        >

        <div class="filter-area">
            <button class="filter-btn active" data-category="all">전체</button>

            {% for category in categories %}
                <button class="filter-btn" data-category="{{ category }}">
                    {{ category }}
                </button>
            {% endfor %}

            <button class="filter-btn" data-category="favorites">
                즐겨찾기 ★
            </button>
        </div>

        <div class="site-grid" id="siteGrid">
            {% for site in sites %}
            <article
                class="site-card"
                data-name="{{ site.name }}"
                data-category="{{ site.category }}"
                data-description="{{ site.description }}"
            >
                <button
                    class="favorite-btn"
                    type="button"
                    aria-label="{{ site.name }} 즐겨찾기"
                    data-favorite="{{ site.name }}"
                >♡</button>

                <div class="card-top">
                    <div class="site-icon">{{ site.icon }}</div>
                    <div>
                        <div class="site-name">{{ site.name }}</div>
                        <div class="site-category">{{ site.category }}</div>
                    </div>
                </div>

                <p class="site-description">{{ site.description }}</p>

                <div class="card-bottom">
                    <span class="site-tag">{{ site.tag }}</span>
                    <a
                        class="visit-btn"
                        href="{{ site.url }}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >사이트 방문 ↗</a>
                </div>
            </article>
            {% endfor %}
        </div>

        <div class="empty-message" id="emptyMessage">
            검색 결과가 없습니다.
        </div>

        <section class="intro">
            <h2>LINK EKKO 주소모아</h2>
            <p>
                LINK EKKO는 OTT·동영상 분야의 사이트 주소를 한곳에 모아
                편리하게 확인할 수 있도록 돕는 링크 모음 서비스입니다.
                검색 기능을 이용해 원하는 사이트를 빠르게 찾아보세요.
                외부 사이트의 서비스 내용과 이용 조건은 각 사이트에서 확인해 주세요.
                LINK EKKO는 외부 사이트의 운영 주체나 공식 제휴사가 아닙니다.
            </p>
        </section>

        <!-- 광고문의 텔레그램 -->

        <section class="contact-section">
            <h2>광고 <span>문의</span></h2>
            <p>
                LINK EKKO 광고 및 제휴 관련 문의는<br>
                아래 텔레그램으로 연락해 주세요.
            </p>

            <a
                class="telegram-btn"
                href="https://t.me/linkekko369"
                target="_blank"
                rel="noopener noreferrer"
            >
                <span class="telegram-icon">✈</span>
                텔레그램으로 문의하기
            </a>

            <span class="telegram-id">@linkekko369</span>
        </section>
    </main>

    <footer>
        <strong>LINK EKKO</strong><br>
        링크 에코 주소모아<br>
        본 사이트는 외부 사이트의 링크를 제공하며,
        각 외부 사이트의 운영 및 콘텐츠에 대한 책임은 해당 사이트에 있습니다.
        <br>
        광고문의: @linkekko369
        <br>
        © 2026 LINK EKKO. All rights reserved.
    </footer>

    <script>
        const searchInput = document.getElementById("searchInput");
        const cards = Array.from(document.querySelectorAll(".site-card"));
        const filterButtons = document.querySelectorAll(".filter-btn");
        const emptyMessage = document.getElementById("emptyMessage");

        let activeCategory = "all";
        let favorites = [];

        try {
            favorites = JSON.parse(
                localStorage.getItem("linkekko_favorites") || "[]"
            );

            if (!Array.isArray(favorites)) {
                favorites = [];
            }
        } catch (error) {
            favorites = [];
        }

        function updateFavoriteButtons() {
            document.querySelectorAll(".favorite-btn").forEach(button => {
                const name = button.dataset.favorite;
                const isFavorite = favorites.includes(name);

                button.classList.toggle("active", isFavorite);
                button.textContent = isFavorite ? "♥" : "♡";
            });
        }

        function filterCards() {
            const keyword = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            cards.forEach(card => {
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                const description = card.dataset.description.toLowerCase();

                const matchesSearch =
                    name.includes(keyword) ||
                    category.includes(keyword) ||
                    description.includes(keyword);

                const matchesCategory =
                    activeCategory === "all" ||
                    (
                        activeCategory === "favorites"
                        ? favorites.includes(card.dataset.name)
                        : card.dataset.category === activeCategory
                    );

                const visible = matchesSearch && matchesCategory;

                card.style.display = visible ? "flex" : "none";

                if (visible) {
                    visibleCount++;
                }
            });

            emptyMessage.style.display =
                visibleCount === 0 ? "block" : "none";
        }

        searchInput.addEventListener("input", filterCards);

        filterButtons.forEach(button => {
            button.addEventListener("click", () => {
                filterButtons.forEach(item =>
                    item.classList.remove("active")
                );

                button.classList.add("active");
                activeCategory = button.dataset.category;
                filterCards();
            });
        });

        document.querySelectorAll(".favorite-btn").forEach(button => {
            button.addEventListener("click", () => {
                const name = button.dataset.favorite;

                if (favorites.includes(name)) {
                    favorites = favorites.filter(item => item !== name);
                } else {
                    favorites.push(name);
                }

                localStorage.setItem(
                    "linkekko_favorites",
                    JSON.stringify(favorites)
                );

                updateFavoriteButtons();
                filterCards();
            });
        });

        updateFavoriteButtons();
        filterCards();
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
        categories=CATEGORIES,
        structured_data=STRUCTURED_DATA
    )


# =====================================
# 사이트맵
# =====================================

@app.route("/sitemap.xml")
def sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{BASE_URL}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
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
    app.run(host="0.0.0.0", port=5000, debug=False)
