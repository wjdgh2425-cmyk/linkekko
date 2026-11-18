
from flask import Flask, render_template_string

app = Flask(__name__)

SITES = [
    {
        "category": "공공기관",
        "name": "정부24",
        "description": "민원 신청과 정부 서비스를 이용하는 공식 사이트",
        "url": "https://www.gov.kr"
    },
    {
        "category": "공공기관",
        "name": "국세청",
        "description": "세금 신고와 국세 관련 서비스",
        "url": "https://www.nts.go.kr"
    },
    {
        "category": "공공기관",
        "name": "국민건강보험",
        "description": "건강보험 관련 정보와 민원 서비스",
        "url": "https://www.nhis.or.kr"
    },
    {
        "category": "교육",
        "name": "한국장학재단",
        "description": "국가장학금과 학자금 지원 정보",
        "url": "https://www.kosaf.go.kr"
    },
    {
        "category": "취업",
        "name": "고용24",
        "description": "일자리 검색과 고용 관련 서비스",
        "url": "https://www.work24.go.kr"
    },
    {
        "category": "창업",
        "name": "K-스타트업",
        "description": "창업 지원 사업과 창업 정보",
        "url": "https://www.k-startup.go.kr"
    }
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
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #20283a;
}
header {
    background: #17233d;
    color: white;
    padding: 28px 20px;
    text-align: center;
}
header h1 {
    margin: 0;
    font-size: 32px;
    letter-spacing: 2px;
}
header p { color: #cbd5e1; }
main {
    max-width: 1000px;
    margin: 35px auto;
    padding: 0 20px;
}
.intro { text-align: center; margin-bottom: 28px; }
.search {
    width: 100%;
    padding: 16px;
    border: 1px solid #d7dce5;
    border-radius: 12px;
    font-size: 16px;
    margin-bottom: 20px;
}
.categories {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 25px;
}
.categories button {
    border: 0;
    background: #e4e9f2;
    padding: 10px 17px;
    border-radius: 20px;
    cursor: pointer;
}
.categories button.active {
    background: #3159c9;
    color: white;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
}
.site {
    background: white;
    padding: 22px;
    border-radius: 15px;
    box-shadow: 0 4px 15px #17233d10;
}
.site small { color: #3159c9; font-weight: bold; }
.site h2 { margin-bottom: 8px; }
.site p { color: #687386; line-height: 1.6; }
.site a {
    display: inline-block;
    margin-top: 10px;
    color: white;
    background: #3159c9;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
}
footer {
    text-align: center;
    color: #8992a2;
    padding: 35px;
}
</style>
</head>
<body>
<header>
    <h1>LINK EKKO</h1>
    <p>필요한 공식 사이트를 한곳에, 주소모아</p>
</header>

<main>
    <section class="intro">
        <h2>원하는 사이트를 빠르게 찾아보세요</h2>
        <p>분야별 공식 사이트와 접속 주소를 한눈에 확인하세요.</p>
    </section>

    <input
        id="search"
        class="search"
        type="text"
        placeholder="사이트 이름이나 분야를 검색하세요..."
        oninput="filterSites()"
    >

    <div class="categories">
        <button class="active" onclick="chooseCategory('전체', this)">전체</button>
        <button onclick="chooseCategory('공공기관', this)">공공기관</button>
        <button onclick="chooseCategory('교육', this)">교육</button>
        <button onclick="chooseCategory('취업', this)">취업</button>
        <button onclick="chooseCategory('창업', this)">창업</button>
    </div>

    <section class="grid" id="siteGrid">
        {% for site in sites %}
        <article class="site"
            data-category="{{ site.category }}"
            data-search="{{ site.name }} {{ site.category }} {{ site.description }}">
            <small>{{ site.category }}</small>
            <h2>{{ site.name }}</h2>
            <p>{{ site.description }}</p>
            <a href="{{ site.url }}" target="_blank" rel="noopener noreferrer">
                공식 사이트 방문하기 ↗
            </a>
        </article>
        {% endfor %}
    </section>
    <p id="empty" style="display:none; text-align:center;">
        검색 결과가 없습니다.
    </p>
</main>

<footer>
    LINK EKKO · 주소모아
</footer>

<script>
let selectedCategory = "전체";

function chooseCategory(category, button) {
    selectedCategory = category;
    document.querySelectorAll(".categories button").forEach(btn => {
        btn.classList.remove("active");
    });
    button.classList.add("active");
    filterSites();
}

function filterSites() {
    const keyword = document.getElementById("search").value.toLowerCase();
    const cards = document.querySelectorAll(".site");
    let visible = 0;

    cards.forEach(card => {
        const category = card.dataset.category;
        const content = card.dataset.search.toLowerCase();

        const categoryMatch =
            selectedCategory === "전체" || category === selectedCategory;
        const keywordMatch = content.includes(keyword);

        if (categoryMatch && keywordMatch) {
            card.style.display = "block";
            visible++;
        } else {
            card.style.display = "none";
        }
    });

    document.getElementById("empty").style.display =
        visible === 0 ? "block" : "none";
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, sites=SITES)

if __name__ == "__main__":
    app.run(debug=True)
