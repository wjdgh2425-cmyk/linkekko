
from flask import Flask, render_template_string, Response, redirect, abort
from datetime import datetime, timezone
import sqlite3
import os

app = Flask(__name__)

BASE_URL = "https://linkekko.onrender.com"

DB_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(app.instance_path, "linkekko.db")
)

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# =====================================
# 사이트 목록
# =====================================

SITES = [
    # OTT · 동영상
    {"name": "티빙", "category": "OTT·동영상", "description": "드라마, 예능, 영화와 실시간 TV", "url": "https://www.tving.com/", "domain": "tving.com", "icon": "📺", "rank": 5},
    {"name": "넷플릭스", "category": "OTT·동영상", "description": "다양한 영화와 오리지널 시리즈", "url": "https://www.netflix.com/kr", "domain": "netflix.com", "icon": "🎬", "rank": 2},
    {"name": "왓챠", "category": "OTT·동영상", "description": "영화와 드라마 감상 서비스", "url": "https://watcha.com/", "domain": "watcha.com", "icon": "🍿"},
    {"name": "쿠팡플레이", "category": "OTT·동영상", "description": "영화, 드라마, 스포츠 콘텐츠", "url": "https://www.coupangplay.com/", "domain": "coupangplay.com", "icon": "🎥", "rank": 9},
    {"name": "유튜브", "category": "OTT·동영상", "description": "다양한 영상과 크리에이터 콘텐츠", "url": "https://www.youtube.com/", "domain": "youtube.com", "icon": "▶️", "rank": 1},
    {"name": "웨이브", "category": "OTT·동영상", "description": "방송 프로그램과 영화 감상", "url": "https://www.wavve.com/", "domain": "wavve.com", "icon": "🌊"},
    {"name": "디즈니플러스", "category": "OTT·동영상", "description": "디즈니, 마블, 스타워즈 콘텐츠", "url": "https://www.disneyplus.com/ko-kr", "domain": "disneyplus.com", "icon": "✨", "rank": 8},
    {"name": "라프텔", "category": "OTT·동영상", "description": "애니메이션 전문 스트리밍", "url": "https://laftel.net/", "domain": "laftel.net", "icon": "🌸"},

    # 게임
    {"name": "넥슨", "category": "게임", "description": "다양한 온라인 게임과 게임 소식", "url": "https://www.nexon.com/", "domain": "nexon.com", "icon": "🎮"},
    {"name": "라이엇 게임즈", "category": "게임", "description": "리그 오브 레전드와 라이엇 게임", "url": "https://www.riotgames.com/", "domain": "riotgames.com", "icon": "⚔️"},
    {"name": "스팀", "category": "게임", "description": "PC 게임 구매와 라이브러리", "url": "https://store.steampowered.com/", "domain": "steampowered.com", "icon": "🕹️", "rank": 3},
    {"name": "플레이스테이션", "category": "게임", "description": "플레이스테이션 게임과 콘솔 정보", "url": "https://www.playstation.com/ko-kr/", "domain": "playstation.com", "icon": "🎯"},
    {"name": "닌텐도", "category": "게임", "description": "닌텐도 게임과 콘솔 정보", "url": "https://www.nintendo.com/kr/", "domain": "nintendo.com", "icon": "🍄"},
    {"name": "배틀그라운드", "category": "게임", "description": "배틀그라운드 공식 홈페이지", "url": "https://pubg.com/ko-kr", "domain": "pubg.com", "icon": "🔫", "rank": 7},

    # 실시간 방송
    {"name": "SOOP", "category": "실시간 방송", "description": "실시간 방송과 스트리머 콘텐츠", "url": "https://www.sooplive.co.kr/", "domain": "sooplive.co.kr", "icon": "📡"},
    {"name": "치지직", "category": "실시간 방송", "description": "게임과 다양한 실시간 방송", "url": "https://chzzk.naver.com/", "domain": "chzzk.naver.com", "icon": "🟢", "rank": 6},
    {"name": "유튜브 라이브", "category": "실시간 방송", "description": "유튜브 실시간 스트리밍", "url": "https://www.youtube.com/live", "domain": "youtube.com", "icon": "🔴"},
    {"name": "틱톡", "category": "실시간 방송", "description": "숏폼 영상과 라이브 방송", "url": "https://www.tiktok.com/", "domain": "tiktok.com", "icon": "🎵"},
    {"name": "킥", "category": "실시간 방송", "description": "글로벌 실시간 스트리밍 플랫폼", "url": "https://kick.com/", "domain": "kick.com", "icon": "💚"},

    # 만화 · 웹툰
    {"name": "네이버웹툰", "category": "만화·웹툰", "description": "다양한 장르의 인기 웹툰", "url": "https://comic.naver.com/", "domain": "comic.naver.com", "icon": "📗", "rank": 4},
    {"name": "카카오웹툰", "category": "만화·웹툰", "description": "인기 웹툰과 독점 연재 작품", "url": "https://webtoon.kakao.com/", "domain": "webtoon.kakao.com", "icon": "📙"},
    {"name": "카카오페이지", "category": "만화·웹툰", "description": "웹툰과 웹소설 콘텐츠", "url": "https://page.kakao.com/", "domain": "page.kakao.com", "icon": "📚", "rank": 10},
    {"name": "네이버 시리즈", "category": "만화·웹툰", "description": "웹툰과 웹소설 감상", "url": "https://series.naver.com/", "domain": "series.naver.com", "icon": "📖"},
    {"name": "레진코믹스", "category": "만화·웹툰", "description": "다양한 장르의 웹툰 플랫폼", "url": "https://www.lezhin.com/", "domain": "lezhin.com", "icon": "🎨"},
    {"name": "봄툰", "category": "만화·웹툰", "description": "다양한 장르의 웹툰 플랫폼", "url": "https://www.bomtoon.com/", "domain": "bomtoon.com", "icon": "🌷"},
    {"name": "리디", "category": "만화·웹툰", "description": "웹툰, 웹소설과 전자책", "url": "https://ridibooks.com/", "domain": "ridibooks.com", "icon": "📕"},
    {"name": "미스터블루", "category": "만화·웹툰", "description": "만화와 웹툰 콘텐츠", "url": "https://www.mrblue.com/", "domain": "mrblue.com", "icon": "🖌️"},
]

CATEGORIES = [
    "전체",
    "OTT·동영상",
    "게임",
    "실시간 방송",
    "만화·웹툰"
]

for index, site in enumerate(SITES):
    site["id"] = index


# =====================================
# 데이터베이스
# =====================================

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS site_visits (
                site_id INTEGER PRIMARY KEY,
                site_name TEXT NOT NULL,
                visit_count INTEGER NOT NULL DEFAULT 0
            )
        """)


init_db()


def get_visit_counts():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT site_id, visit_count FROM site_visits"
        ).fetchall()

    return {
        row["site_id"]: row["visit_count"]
        for row in rows
    }


def get_ranked_sites():
    counts = get_visit_counts()
    ranked = []

    for site in SITES:
        item = site.copy()
        item["visit_count"] = counts.get(site["id"], 0)
        ranked.append(item)

    ranked.sort(
        key=lambda site: (
            -site["visit_count"],
            site.get("rank", 999)
        )
    )

    return ranked


# =====================================
# 홈페이지 디자인
# =====================================

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>링크에코 | 분야별 공식 사이트 주소모아</title>

<meta name="description" content="링크에코는 OTT·동영상, 게임, 실시간 방송, 만화·웹툰 분야의 공식 사이트 주소와 실제 방문 기록 기반 인기 순위를 제공하는 주소모아 서비스입니다.">
<meta name="keywords" content="링크에코, 주소모아, 인기사이트, 공식사이트, OTT, 게임, 실시간방송, 만화, 웹툰">
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="pPTsfFdNbqdZlwp9cF4Bp_mVbMWP-YJ_HMiEBsNr7B4">

<link rel="canonical" href="https://linkekko.onrender.com/">

<meta property="og:type" content="website">
<meta property="og:title" content="링크에코 | 분야별 공식 사이트 주소모아">
<meta property="og:description" content="자주 찾는 공식 사이트와 인기 사이트를 링크에코에서 확인하세요.">
<meta property="og:url" content="https://linkekko.onrender.com/">
<meta property="og:site_name" content="링크에코">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "링크에코",
  "url": "https://linkekko.onrender.com/",
  "description": "분야별 공식 사이트 주소와 인기 사이트를 모아 제공하는 주소모아 서비스"
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
        radial-gradient(circle at 15% 10%, rgba(94,48,180,0.23), transparent 35%),
        radial-gradient(circle at 85% 20%, rgba(0,145,255,0.16), transparent 35%),
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
    background: rgba(8,11,24,0.75);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 10;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(90deg,#a78bfa,#38bdf8);
    -webkit-background-clip: text;
    color: transparent;
}

.header-contact {
    font-size: 13px;
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.4);
    padding: 9px 15px;
    border-radius: 20px;
}

.header-contact:hover {
    background: rgba(139,92,246,0.2);
}

/* 에코 배경 */

.hero {
    text-align: center;
    padding: 100px 20px 65px;
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(
            90deg,
            rgba(8,11,24,0.92) 0%,
            rgba(8,11,24,0.65) 40%,
            rgba(8,11,24,0.12) 100%
        ),
        url("https://skins.nerfplz.com/art/245019_splash.jpg");
    background-size: cover;
    background-position: center 18%;
    background-repeat: no-repeat;
    min-height: 650px;
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
    font-size: clamp(36px,6vw,62px);
    margin: 0 0 18px;
    font-weight: 900;
    letter-spacing: -2px;
}

.hero h1 span {
    background: linear-gradient(90deg,#a78bfa,#38bdf8);
    -webkit-background-clip: text;
    color: transparent;
}

.hero p {
    color: #d0d5e5;
    line-height: 1.8;
    font-size: 15px;
    margin: 0 auto 25px;
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
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    color: white;
    border: none;
    padding: 0 22px;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
}

/* GIANTS 음악 플레이어 */

.music-section {
    width: min(440px, 100%);
    margin: 28px auto 0;
    padding: 17px;
    border: 1px solid rgba(167,139,250,0.38);
    border-radius: 18px;
    background: rgba(8,11,24,0.82);
    box-shadow: 0 0 30px rgba(124,58,237,0.2);
    backdrop-filter: blur(10px);
}

.music-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 5px;
}

.music-artist {
    font-size: 11px;
    color: #a5b4fc;
    margin-bottom: 14px;
}

.music-frame {
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    border-radius: 12px;
    background: #080b18;
}

.music-frame iframe {
    width: 100%;
    height: 100%;
    border: 0;
}

.music-button {
    width: 100%;
    margin-top: 12px;
    padding: 12px 15px;
    border: 0;
    border-radius: 10px;
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    color: white;
    font-weight: bold;
    cursor: pointer;
    font-size: 13px;
}

.music-status {
    color: #aab3cc;
    font-size: 11px;
    line-height: 1.6;
    margin-top: 10px;
}

/* 본문 */

.container {
    max-width: 1150px;
    margin: 0 auto;
    padding: 20px 22px 70px;
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

/* 인기 순위 */

.popular-section {
    margin-top: 12px;
    margin-bottom: 55px;
}

.popular-subtitle {
    color: #929bb4;
    font-size: 12px;
    margin: 8px 0 20px;
    line-height: 1.7;
}

.popular-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0,1fr));
    gap: 14px;
}

.popular-card {
    background: linear-gradient(145deg,#1b2038,#101527);
    border: 1px solid rgba(148,163,184,0.13);
    border-radius: 16px;
    padding: 17px 13px;
    min-width: 0;
    transition: 0.25s;
    display: flex;
    flex-direction: column;
}

.popular-card:hover {
    transform: translateY(-5px);
    border-color: rgba(139,92,246,0.65);
    box-shadow: 0 10px 30px rgba(76,29,149,0.18);
}

.rank-number {
    font-size: 12px;
    font-weight: 900;
    color: #a78bfa;
    margin-bottom: 12px;
}

.rank-number.top-three {
    color: #fbbf24;
}

.popular-logo-area {
    width: 54px;
    height: 54px;
    background: #fff;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 7px;
    overflow: hidden;
    margin-bottom: 13px;
}

.popular-logo {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.popular-icon {
    display: none;
    font-size: 27px;
}

.popular-card h3 {
    font-size: 14px;
    margin: 0 0 7px;
}

.popular-card p {
    color: #929bb4;
    font-size: 11px;
    line-height: 1.6;
    min-height: 34px;
    margin: 0 0 10px;
    flex: 1;
}

.popular-count {
    color: #c4b5fd;
    font-size: 11px;
    margin-bottom: 12px;
}

.popular-link {
    color: #a5b4fc;
    font-size: 11px;
    font-weight: bold;
}

/* 카테고리 */

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
    background: linear-gradient(135deg,#6d28d9,#2563eb);
    border-color: transparent;
}

/* 사이트 카드 */

.site-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill,minmax(220px,1fr));
    gap: 16px;
}

.site-card {
    background: linear-gradient(145deg,#171d32,#101527);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 17px;
    padding: 21px;
    min-height: 190px;
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
    min-height: 55px;
    margin-bottom: 15px;
}

.logo-area {
    width: 54px;
    height: 54px;
    border-radius: 13px;
    background: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding: 7px;
    flex-shrink: 0;
}

.site-logo {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.site-icon-fallback {
    font-size: 28px;
    display: none;
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
    margin: 0 0 10px;
    flex: 1;
}

.site-visit-count {
    font-size: 11px;
    color: #a5acc2;
    margin-bottom: 12px;
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

/* 소개 */

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

/* 하단 */

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

/* 모바일 */

@media (max-width: 850px) {
    .popular-grid {
        grid-template-columns: repeat(3,minmax(0,1fr));
    }
}

@media (max-width: 600px) {
    header {
        padding: 17px 5%;
    }

    .logo {
        font-size: 21px;
    }

    .hero {
        padding: 75px 18px 45px;
        min-height: 540px;
        background-position: 58% top;
        background-size: auto 100%;
    }

    .popular-grid {
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 10px;
    }

    .popular-card {
        padding: 14px 12px;
    }

    .site-grid {
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 10px;
    }

    .site-card {
        padding: 15px;
        min-height: 185px;
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

    .logo-area,
    .popular-logo-area {
        width: 48px;
        height: 48px;
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

        <!-- 트루 데미지 GIANTS 음악 -->

        <section class="music-section" aria-label="링크에코 배경 음악">

            <div class="music-title">🎵 링크에코 대표 음악</div>
            <div class="music-artist">TRUE DAMAGE - GIANTS</div>

            <div class="music-frame">
                <div id="giants-player"></div>
            </div>

            <button
                type="button"
                class="music-button"
                id="musicButton"
                onclick="startMusic()"
            >
                ▶ 음악 재생하기
            </button>

            <div class="music-status" id="musicStatus">
                페이지 접속 시 자동 재생을 시도합니다.
                자동 재생이 차단되면 재생 버튼을 눌러주세요.
            </div>

        </section>

    </div>
</section>

<main class="container">

    <section class="popular-section">

        <div class="section-heading">
            <h2>🔥 인기 사이트 TOP 10</h2>
        </div>

        <p class="popular-subtitle">
            링크에코에서 발생한 사이트 방문 횟수를 기준으로 자동 정렬됩니다.
        </p>

        <div class="popular-grid">

            {% for site in popular_sites %}
            <a class="popular-card" href="/go/{{ site.id }}">

                <div class="rank-number {% if loop.index <= 3 %}top-three{% endif %}">
                    TOP {{ loop.index }}
                </div>

                <div class="popular-logo-area">

                    <img
                        class="popular-logo"
                        src="https://www.google.com/s2/favicons?domain={{ site.domain }}&sz=128"
                        alt="{{ site.name }} 로고"
                        loading="lazy"
                        onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                    >

                    <span class="popular-icon">{{ site.icon }}</span>

                </div>

                <h3>{{ site.name }}</h3>
                <p>{{ site.description }}</p>

                <div class="popular-count">
                    누적 방문 {{ "{:,}".format(site.visit_count) }}회
                </div>

                <span class="popular-link">공식 사이트 방문 →</span>

            </a>
            {% endfor %}

        </div>

    </section>

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

                <div class="logo-area">

                    <img
                        class="site-logo"
                        src="https://www.google.com/s2/favicons?domain={{ site.domain }}&sz=128"
                        alt="{{ site.name }} 로고"
                        loading="lazy"
                        onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                    >

                    <span class="site-icon-fallback">
                        {{ site.icon }}
                    </span>

                </div>

                <button
                    class="favorite"
                    aria-label="{{ site.name }} 즐겨찾기"
                    onclick="toggleFavorite('{{ site.name }}', this)"
                >☆</button>

            </div>

            <h3>{{ site.name }}</h3>
            <p>{{ site.description }}</p>

            <div class="site-visit-count">
                누적 방문 {{ "{:,}".format(site.visit_count) }}회
            </div>

            <a class="visit-link" href="/go/{{ site.id }}">
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
            편리하게 관리할 수 있으며, 실제 방문 기록을 바탕으로
            인기 사이트 순위를 제공합니다.
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
/* =====================================
   GIANTS 유튜브 자동 재생
===================================== */

let giantsPlayer;
let musicReady = false;

function onYouTubeIframeAPIReady() {
    giantsPlayer = new YT.Player("giants-player", {
        videoId: "sVZpHFXcFJw",

        playerVars: {
            autoplay: 1,
            controls: 1,
            playsinline: 1,
            rel: 0
        },

        events: {
            onReady: function(event) {
                musicReady = true;

                // 페이지 접속 시 소리와 함께 자동 재생 시도
                event.target.unMute();
                event.target.setVolume(70);
                event.target.playVideo();

                document.getElementById("musicStatus").textContent =
                    "GIANTS 자동 재생을 시도하고 있습니다.";
            },

            onStateChange: function(event) {
                const button = document.getElementById("musicButton");
                const status = document.getElementById("musicStatus");

                if (event.data === YT.PlayerState.PLAYING) {
                    button.style.display = "none";
                    status.textContent = "♪ TRUE DAMAGE - GIANTS 재생 중";
                }

                if (
                    event.data === YT.PlayerState.PAUSED ||
                    event.data === YT.PlayerState.ENDED
                ) {
                    button.style.display = "block";
                    button.textContent = "▶ 음악 재생하기";
                    status.textContent = "음악이 일시정지되었습니다.";
                }
            },

            onAutoplayBlocked: function() {
                showMusicButton();
            },

            onError: function() {
                showMusicButton();
                document.getElementById("musicStatus").textContent =
                    "음악을 불러오지 못했습니다. 잠시 후 다시 시도해주세요.";
            }
        }
    });
}

function showMusicButton() {
    document.getElementById("musicButton").style.display = "block";
    document.getElementById("musicStatus").textContent =
        "브라우저가 자동 재생을 차단했습니다. 아래 버튼을 눌러 음악을 재생해주세요.";
}

function startMusic() {
    if (!musicReady || !giantsPlayer) {
        document.getElementById("musicStatus").textContent =
            "음악 플레이어를 준비하고 있습니다. 잠시 후 다시 눌러주세요.";
        return;
    }

    giantsPlayer.unMute();
    giantsPlayer.setVolume(70);
    giantsPlayer.playVideo();

    document.getElementById("musicStatus").textContent =
        "GIANTS 재생을 요청했습니다.";
}

// 유튜브 공식 플레이어 API 불러오기
const youtubeScript = document.createElement("script");
youtubeScript.src = "https://www.youtube.com/iframe_api";
document.head.appendChild(youtubeScript);


/* =====================================
   사이트 검색 및 카테고리
===================================== */

let currentCategory = "전체";
let favoritesOnly = false;

function getCards() {
    return Array.from(
        document.querySelectorAll("#siteGrid .site-card")
    );
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


/* =====================================
   즐겨찾기
===================================== */

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
    ranked_sites = get_ranked_sites()

    return render_template_string(
        HTML,
        sites=ranked_sites,
        categories=CATEGORIES,
        popular_sites=ranked_sites[:10]
    )


# =====================================
# 사이트 클릭 기록 후 이동
# =====================================

@app.route("/go/<int:site_id>")
def visit_site(site_id):

    if site_id < 0 or site_id >= len(SITES):
        abort(404)

    site = SITES[site_id]

    with get_db() as conn:
        conn.execute("""
            INSERT INTO site_visits (site_id, site_name, visit_count)
            VALUES (?, ?, 1)
            ON CONFLICT(site_id)
            DO UPDATE SET
                site_name = excluded.site_name,
                visit_count = visit_count + 1
        """, (site_id, site["name"]))

    return redirect(site["url"])


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
