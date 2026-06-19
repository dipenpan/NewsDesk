#############################################################################
# app.py
#
# Streamlit entrypoint for NewsDesk, a professional news reader app.
#
#############################################################################

from datetime import datetime
from html import escape
from pathlib import Path
import sqlite3
import tempfile

import streamlit as st


VIEWS = ["Feed", "Reader", "Saved", "About"]
SECTIONS = ["Top Stories", "Technology", "Health", "Education"]
DB_PATH = Path(tempfile.gettempdir()) / "newsdesk.db"
LOCAL_READER_ID = "local-reader"
DEFAULT_POLL = {"Very useful": 12, "Somewhat useful": 7, "Not useful": 2}

ARTICLES = [
    {
        "id": "ai-grid",
        "section": "Technology",
        "top_story": True,
        "title": "Cities Turn to AI to Predict Pressure on the Power Grid",
        "dek": (
            "Utility teams are testing forecasting systems that combine weather, "
            "building demand, and outage reports to prepare for peak usage."
        ),
        "author": "Maya Chen",
        "published": "June 9, 2026",
        "read_time": "5 min read",
        "image": "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1400&q=80",
        "body": [
            "Several midsize cities are piloting machine-learning tools that flag neighborhoods likely to face elevated electricity demand before temperatures spike. The goal is not to replace utility operators, but to give them earlier signals for staffing, maintenance, and public alerts.",
            "The systems pull from weather forecasts, historical usage, building data, and customer outage reports. Officials say the models are most useful when they explain why a recommendation was made, such as a predicted heat index combined with an unusual commercial load pattern.",
            "Privacy advocates have urged cities to publish clear data-use rules before expanding the programs. Utility leaders say the next phase will focus on independent audits and clearer dashboards for residents.",
        ],
        "summary": [
            "Cities are testing AI tools to forecast power-grid stress before demand peaks.",
            "The most useful systems combine weather, historical usage, and outage reports.",
            "Experts want stronger transparency rules before the tools expand.",
        ],
        "tags": ["AI", "Infrastructure", "Public Policy"],
        "source": "Metro Systems Review",
        "credibility": 94,
    },
    {
        "id": "chip-supply",
        "section": "Technology",
        "top_story": True,
        "title": "Chip Makers Race to Cut Energy Use in Data Centers",
        "dek": "New processor designs focus on lowering power demand as AI workloads grow.",
        "author": "Elena Morris",
        "published": "June 9, 2026",
        "read_time": "4 min read",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1400&q=80",
        "body": [
            "Semiconductor companies are redesigning server chips around energy efficiency as data-center operators face rising power costs and tighter grid constraints.",
            "The latest designs use specialized accelerators, improved cooling support, and software controls that shift workloads away from peak-demand windows.",
            "Analysts say performance is still important, but buyers are now asking more detailed questions about watts per task and long-term operating costs.",
        ],
        "summary": [
            "Chip companies are prioritizing energy efficiency for AI data centers.",
            "New designs combine accelerators, cooling improvements, and workload controls.",
            "Customers are evaluating chips by operating cost, not just raw speed.",
        ],
        "tags": ["Chips", "AI", "Data Centers"],
        "source": "Compute Market Daily",
        "credibility": 91,
    },
    {
        "id": "housing-costs",
        "section": "Top Stories",
        "top_story": True,
        "title": "Rent Growth Slows as New Apartments Reach the Market",
        "dek": "Analysts say supply is helping cool prices, but affordability remains uneven.",
        "author": "Jordan Hale",
        "published": "June 8, 2026",
        "read_time": "3 min read",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80",
        "body": [
            "New apartment supply is beginning to cool rent growth in several large metro areas, according to analysts tracking lease data across newly opened buildings.",
            "The relief is not evenly distributed. Renters in older suburbs and smaller cities are still seeing elevated costs because fewer units have been added in those markets.",
            "Housing researchers say the next test is whether local governments keep approving new projects after the current construction wave is absorbed.",
        ],
        "summary": [
            "New apartment supply is slowing rent growth in several metro areas.",
            "Affordability is still difficult for lower-income renters.",
            "Economists expect regional differences to remain significant.",
        ],
        "tags": ["Housing", "Economy"],
        "source": "Civic Economy Wire",
        "credibility": 89,
    },
    {
        "id": "health-data",
        "section": "Health",
        "top_story": True,
        "title": "Hospitals Test Shared Dashboards for Emergency Room Wait Times",
        "dek": "Regional networks hope better visibility can reduce bottlenecks.",
        "author": "Priya Nair",
        "published": "June 7, 2026",
        "read_time": "4 min read",
        "image": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80",
        "body": [
            "Hospital networks in several regions are testing shared dashboards that show emergency room wait times, bed availability, and staffing pressure across nearby facilities.",
            "The dashboards are intended to help dispatchers and care teams redirect noncritical patients before bottlenecks become severe.",
            "Administrators say the hardest part is keeping data current enough for real-time decisions without adding more work for clinical staff.",
        ],
        "summary": [
            "Hospitals are coordinating wait-time data.",
            "Dashboards may help reroute noncritical patients.",
            "Accuracy and update speed remain major challenges.",
        ],
        "tags": ["Health", "Data", "Hospitals"],
        "source": "Health Systems Monitor",
        "credibility": 93,
    },
    {
        "id": "mental-health",
        "section": "Health",
        "top_story": False,
        "title": "Schools Expand Mental Health Screening Programs",
        "dek": "Districts are pairing early screening with counseling partnerships.",
        "author": "Marcus Lee",
        "published": "June 6, 2026",
        "read_time": "4 min read",
        "image": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1400&q=80",
        "body": [
            "More school districts are adding voluntary mental health screening programs as student support teams report higher demand for counseling.",
            "The most mature programs pair screening with direct referral paths so families are not left to navigate care options alone.",
            "Researchers say districts need clear consent rules, multilingual communication, and follow-up capacity before expanding screenings.",
        ],
        "summary": [
            "Schools are expanding voluntary mental health screening programs.",
            "Experts say screening only helps when referral support is available.",
            "Consent, privacy, and follow-up capacity remain key concerns.",
        ],
        "tags": ["Mental Health", "Schools", "Youth"],
        "source": "Education Health Brief",
        "credibility": 88,
    },
    {
        "id": "classroom-ai",
        "section": "Education",
        "top_story": True,
        "title": "Teachers Build AI Guidelines Into Everyday Assignments",
        "dek": "Classrooms are shifting from banning AI tools to teaching responsible use.",
        "author": "Riley Grant",
        "published": "June 9, 2026",
        "read_time": "5 min read",
        "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1400&q=80",
        "body": [
            "Teachers are increasingly asking students to document when and how they use AI tools, turning disclosure into part of the assignment rather than treating the tools as automatically off limits.",
            "Some assignments now require students to compare an AI-generated draft with their final work and explain what they changed.",
            "Administrators say the approach gives students practical experience while still preserving expectations around original analysis.",
        ],
        "summary": [
            "Schools are moving from AI bans toward structured usage rules.",
            "Students may be asked to disclose prompts, edits, and final reasoning.",
            "Teachers want AI to support learning without replacing original work.",
        ],
        "tags": ["Education", "AI Literacy", "Classrooms"],
        "source": "Learning Policy Desk",
        "credibility": 92,
    },
    {
        "id": "college-transfer",
        "section": "Education",
        "top_story": False,
        "title": "Community Colleges Streamline Transfer Pathways",
        "dek": "New advising tools aim to reduce lost credits between two-year and four-year programs.",
        "author": "Lena Ortiz",
        "published": "June 5, 2026",
        "read_time": "3 min read",
        "image": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1400&q=80",
        "body": [
            "Community colleges are expanding transfer-planning tools that show students which courses count toward four-year degrees before they register.",
            "Advisers say clearer maps can save students time and money by reducing credits that do not apply to a target major.",
            "State systems are also encouraging colleges to publish transfer outcomes so students can compare pathways more easily.",
        ],
        "summary": [
            "Community colleges are improving transfer maps for students.",
            "The goal is to reduce lost credits and extra tuition costs.",
            "States want clearer public data on transfer outcomes.",
        ],
        "tags": ["Higher Education", "Transfer", "Affordability"],
        "source": "Campus Ledger",
        "credibility": 87,
    },
]

INITIAL_COMMENTS = [
    {
        "id": 1,
        "name": "Alex Rivera",
        "body": "The transparency point matters. If residents cannot see how predictions are made, trust will be low.",
        "time": "10:14 PM",
        "replies": [
            {
                "name": "Sam Patel",
                "body": "Agreed. A public model card would make this easier to evaluate.",
                "time": "10:22 PM",
            }
        ],
    },
    {
        "id": 2,
        "name": "Nina Brooks",
        "body": "This would be useful during heat waves if alerts are clear and early enough.",
        "time": "10:31 PM",
        "replies": [],
    },
]


def connect_db():
    """Opens a SQLite connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Creates database tables and seeds default data."""
    with connect_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_articles (
                user_id TEXT NOT NULL,
                article_id TEXT NOT NULL,
                saved_at TEXT NOT NULL,
                PRIMARY KEY (user_id, article_id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS poll_votes (
                article_id TEXT NOT NULL,
                option_label TEXT NOT NULL,
                vote_count INTEGER NOT NULL,
                PRIMARY KEY (article_id, option_label)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id TEXT NOT NULL,
                parent_id INTEGER,
                name TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(parent_id) REFERENCES comments(id)
            )
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO saved_articles (user_id, article_id, saved_at)
            SELECT ?, article_id, saved_at
            FROM saved_articles
            WHERE user_id = 'guest'
            """,
            (LOCAL_READER_ID,),
        )
        connection.execute(
            "DELETE FROM saved_articles WHERE user_id = 'guest'"
        )

        for article in ARTICLES:
            for option, count in DEFAULT_POLL.items():
                connection.execute(
                    """
                    INSERT OR IGNORE INTO poll_votes (article_id, option_label, vote_count)
                    VALUES (?, ?, ?)
                    """,
                    (article["id"], option, count),
                )

        existing_seed = connection.execute(
            "SELECT COUNT(*) FROM comments WHERE article_id = ?",
            (ARTICLES[0]["id"],),
        ).fetchone()[0]
        if existing_seed == 0:
            for comment in INITIAL_COMMENTS:
                cursor = connection.execute(
                    """
                    INSERT INTO comments (article_id, parent_id, name, body, created_at)
                    VALUES (?, NULL, ?, ?, ?)
                    """,
                    (ARTICLES[0]["id"], comment["name"], comment["body"], comment["time"]),
                )
                parent_id = cursor.lastrowid
                for reply in comment["replies"]:
                    connection.execute(
                        """
                        INSERT INTO comments (article_id, parent_id, name, body, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (ARTICLES[0]["id"], parent_id, reply["name"], reply["body"], reply["time"]),
                    )


def load_saved_article_ids():
    """Loads saved article ids for the local reader."""
    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT article_id
            FROM saved_articles
            WHERE user_id = ?
            ORDER BY saved_at DESC
            """,
            (LOCAL_READER_ID,),
        ).fetchall()
    return [row["article_id"] for row in rows]


def save_article(article_id):
    """Persists a saved article."""
    with connect_db() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO saved_articles (user_id, article_id, saved_at)
            VALUES (?, ?, ?)
            """,
            (LOCAL_READER_ID, article_id, current_time_label()),
        )


def remove_saved_article(article_id):
    """Removes a saved article."""
    with connect_db() as connection:
        connection.execute(
            """
            DELETE FROM saved_articles
            WHERE user_id = ? AND article_id = ?
            """,
            (LOCAL_READER_ID, article_id),
        )


def load_poll_results():
    """Loads poll vote counts for every article."""
    results = {article["id"]: DEFAULT_POLL.copy() for article in ARTICLES}
    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT article_id, option_label, vote_count
            FROM poll_votes
            ORDER BY article_id, option_label
            """
        ).fetchall()
    for row in rows:
        results.setdefault(row["article_id"], DEFAULT_POLL.copy())
        results[row["article_id"]][row["option_label"]] = row["vote_count"]
    return results


def record_vote(article_id, option_label):
    """Increments a poll vote count."""
    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO poll_votes (article_id, option_label, vote_count)
            VALUES (?, ?, 1)
            ON CONFLICT(article_id, option_label)
            DO UPDATE SET vote_count = vote_count + 1
            """,
            (article_id, option_label),
        )


def load_comments():
    """Loads comments and replies grouped by article."""
    comments_by_article = {article["id"]: [] for article in ARTICLES}
    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT id, article_id, parent_id, name, body, created_at
            FROM comments
            ORDER BY id ASC
            """
        ).fetchall()

    comments_by_id = {}
    for row in rows:
        comment = {
            "id": row["id"],
            "name": row["name"],
            "body": row["body"],
            "time": row["created_at"],
            "replies": [],
        }
        comments_by_id[row["id"]] = comment
        if row["parent_id"] is None:
            comments_by_article.setdefault(row["article_id"], []).append(comment)
        elif row["parent_id"] in comments_by_id:
            comments_by_id[row["parent_id"]]["replies"].append(comment)

    return comments_by_article


def add_comment(article_id, name, body):
    """Persists a top-level article comment."""
    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO comments (article_id, parent_id, name, body, created_at)
            VALUES (?, NULL, ?, ?, ?)
            """,
            (article_id, name, body, current_time_label()),
        )


def add_reply(article_id, parent_id, name, body):
    """Persists a reply to a comment."""
    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO comments (article_id, parent_id, name, body, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (article_id, parent_id, name, body, current_time_label()),
        )


def current_time_label():
    """Returns a compact display timestamp."""
    return datetime.now().strftime("%I:%M %p").lstrip("0")


def initialize_state():
    """Initializes local state for the app."""
    initialize_database()
    if "view" not in st.session_state:
        st.session_state.view = "Feed"
    if st.session_state.view == "Bookmarks":
        st.session_state.view = "Saved"
    if st.session_state.view not in VIEWS:
        st.session_state.view = "Feed"
    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "Top Stories"
    if st.session_state.selected_section not in SECTIONS:
        st.session_state.selected_section = "Top Stories"
    if "selected_article" not in st.session_state:
        st.session_state.selected_article = ARTICLES[0]["id"]
    st.session_state.bookmarks = load_saved_article_ids()
    st.session_state.comments_by_article = load_comments()
    st.session_state.poll_by_article = load_poll_results()


def inject_styles():
    """Adds product-style CSS."""
    st.markdown(
        """
        <style>
            :root {
                --bg: #f4f2ec;
                --surface: #fffdf8;
                --panel: #ffffff;
                --panel-2: #f7f1e8;
                --text: #191b1f;
                --muted: #626a73;
                --line: #ded8cc;
                --accent: #0f6b62;
                --accent-2: #b2452d;
                --accent-soft: #e4f1ee;
                --amber-soft: #fff1cf;
                --green: #197a4d;
            }

            .stApp {
                background: var(--bg);
                color: var(--text);
            }

            header[data-testid="stHeader"] {
                background: transparent;
            }

            #MainMenu, footer, .stDeployButton {
                visibility: hidden;
            }

            div[data-testid="stToolbar"] {
                display: none;
            }

            section[data-testid="stSidebar"] {
                background: #191b1f !important;
                border-right: 1px solid #31343a !important;
            }

            section[data-testid="stSidebar"] > div {
                background: #191b1f !important;
                padding-top: 1.4rem;
            }

            section[data-testid="stSidebar"] div,
            section[data-testid="stSidebar"] div[data-testid="stSidebarContent"],
            section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"],
            section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"],
            section[data-testid="stSidebar"] div[data-testid="stElementContainer"] {
                background-color: transparent !important;
            }

            section[data-testid="stSidebar"] > div,
            section[data-testid="stSidebar"] div[data-testid="stSidebarContent"],
            section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
                background-color: #191b1f !important;
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
                color: #f7f2e9 !important;
            }

            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
            section[data-testid="stSidebar"] label p,
            section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p {
                color: #cfc7bc !important;
            }

            section[data-testid="stSidebar"] div[data-testid="stMetric"] {
                background: #24272e !important;
                border-color: #3a3d45 !important;
                padding: 12px 16px !important;
            }

            section[data-testid="stSidebar"] div[data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: #ffffff !important;
            }

            section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
                background: #24272e !important;
                border-color: #454953 !important;
                color: #ffffff !important;
            }

            section[data-testid="stSidebar"] div[data-baseweb="select"] span,
            section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
                color: #ffffff !important;
                fill: #ffffff !important;
            }

            [data-testid="collapsedControl"] button,
            button[title="Open sidebar"],
            button[aria-label="Open sidebar"] {
                background: #191b1f !important;
                border: 1px solid #3a3d45 !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 14px rgba(0, 0, 0, .18) !important;
                height: 40px !important;
                opacity: 1 !important;
                position: relative !important;
                width: 40px !important;
            }

            [data-testid="collapsedControl"] button svg,
            button[title="Open sidebar"] svg,
            button[aria-label="Open sidebar"] svg {
                display: none !important;
            }

            [data-testid="collapsedControl"] button::before,
            button[title="Open sidebar"]::before,
            button[aria-label="Open sidebar"]::before {
                color: #ffffff !important;
                content: "ND";
                display: block;
                font-size: 13px;
                font-weight: 900;
                letter-spacing: .04em;
                line-height: 38px;
                text-align: center;
                width: 100%;
            }

            section[data-testid="stSidebar"] [data-testid="stRadio"] label {
                align-items: center !important;
                display: flex !important;
                min-height: 30px !important;
                padding: 2px 0 !important;
            }

            section[data-testid="stSidebar"] [data-testid="stRadio"] label p {
                color: #f7f2e9 !important;
                font-size: 14px !important;
                font-weight: 750 !important;
                margin: 0 !important;
            }

            section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
                gap: 2px !important;
            }

            section[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] {
                margin: 0 !important;
            }

            .sidebar-section-label {
                color: #cfc7bc !important;
                font-size: 13px;
                font-weight: 800;
                margin: 14px 0 4px;
            }

            .sidebar-credit {
                color: #9aa1ad !important;
                font-size: 12px;
                line-height: 1.5;
                margin-top: 14px;
            }

            .block-container {
                max-width: 1120px;
                padding: 1.75rem 1.5rem 3.5rem;
            }

            h1, h2, h3, h4 {
                color: var(--text);
                letter-spacing: 0;
            }

            p,
            label,
            [data-testid="stMarkdownContainer"],
            [data-testid="stWidgetLabel"] p,
            [data-testid="stCaptionContainer"],
            [data-testid="stRadio"] label p {
                color: var(--text) !important;
            }

            [data-testid="stCaptionContainer"] {
                color: var(--muted) !important;
                font-weight: 650;
            }

            a {
                color: var(--accent);
            }

            .brand-kicker {
                color: var(--accent);
                font-size: 13px;
                font-weight: 700;
                letter-spacing: .08em;
                text-transform: uppercase;
            }

            .masthead {
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 8px;
                margin-bottom: 1rem;
                padding: 22px 24px;
            }

            .masthead h1 {
                font-size: 38px;
                line-height: 1.1;
                margin-bottom: 8px;
            }

            .masthead-copy {
                color: var(--muted);
                font-size: 16px;
                line-height: 1.5;
                margin: 0;
                max-width: 720px;
            }

            .hero-image {
                aspect-ratio: 16 / 7;
                border-radius: 8px;
                display: block;
                object-fit: cover;
                width: 100%;
            }

            .feed-image {
                aspect-ratio: 16 / 10;
                border-radius: 8px;
                display: block;
                object-fit: cover;
                width: 100%;
            }

            .related-image {
                aspect-ratio: 16 / 9;
                border-radius: 8px;
                display: block;
                object-fit: cover;
                max-width: 100%;
                width: 100%;
            }

            .eyebrow {
                color: var(--accent);
                font-size: 12px;
                font-weight: 850;
                letter-spacing: .09em;
                margin: 0 0 8px;
                text-transform: uppercase;
            }

            .dek {
                color: #454b52;
                font-size: 20px;
                line-height: 1.45;
                margin: 0 0 16px;
            }

            .article-body {
                color: #282c31;
                font-size: 18px;
                line-height: 1.75;
            }

            .muted {
                color: var(--muted) !important;
                font-size: 14px;
            }

            .story-meta {
                color: var(--muted);
                font-size: 13px;
                font-weight: 650;
                margin: 12px 0 14px;
            }

            .feed-card-body {
                padding: 4px 0;
            }

            .section-heading {
                margin: 26px 0 12px;
            }

            .tag {
                background: var(--accent-soft);
                border: 1px solid #afd7cf;
                border-radius: 999px;
                color: #0b514b;
                display: inline-block;
                font-size: 12px;
                font-weight: 750;
                margin: 0 8px 8px 0;
                padding: 5px 10px;
            }

            div[data-testid="stMetric"] {
                background: var(--panel);
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 14px 16px;
            }

            div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
                color: var(--muted) !important;
                font-weight: 700;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--surface) !important;
                border-color: var(--line) !important;
                overflow: hidden;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] > div {
                padding: 16px !important;
            }

            .stButton > button {
                background: #191b1f;
                border: 1px solid #191b1f;
                border-radius: 8px;
                color: #ffffff;
                font-weight: 800;
            }

            .stButton > button *,
            button[kind] *,
            button[data-testid] *,
            button p,
            button span {
                color: #ffffff !important;
            }

            div[data-testid="stFormSubmitButton"] button {
                background: #191b1f !important;
                border: 1px solid #191b1f !important;
                border-radius: 8px !important;
                color: #ffffff !important;
                font-weight: 800 !important;
            }

            div[data-testid="stFormSubmitButton"] button p,
            div[data-testid="stFormSubmitButton"] button span {
                color: #ffffff !important;
            }

            .stButton > button:hover {
                background: var(--accent);
                border-color: var(--accent);
                color: #ffffff;
            }

            .stButton > button:hover *,
            button:hover p,
            button:hover span {
                color: #ffffff !important;
            }

            div[data-testid="stFormSubmitButton"] button:hover {
                background: var(--accent) !important;
                border-color: var(--accent) !important;
                color: #ffffff !important;
            }

            .stButton > button:focus,
            .stButton > button:active {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 2px rgba(15, 107, 98, .22) !important;
                color: #ffffff;
                outline: none !important;
            }

            div[data-testid="stFormSubmitButton"] button:focus,
            div[data-testid="stFormSubmitButton"] button:active,
            div[data-testid="stFormSubmitButton"] button:focus p,
            div[data-testid="stFormSubmitButton"] button:active p {
                color: #ffffff !important;
            }

            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            textarea {
                background: #ffffff;
                border-color: #d6cec0;
                color: var(--text);
            }

            div[data-baseweb="input"] input,
            div[data-baseweb="select"] span,
            textarea {
                color: var(--text);
            }

            div[data-baseweb="input"] input::placeholder,
            textarea::placeholder {
                color: #7d838b;
                opacity: 1;
            }

            [data-testid="stTextArea"] textarea {
                background: #ffffff !important;
                color: var(--text) !important;
            }

            [data-testid="stTextArea"] textarea::placeholder {
                color: #7d838b !important;
                opacity: 1;
            }

            [data-testid="stAlert"] {
                background: #e8f3ff;
                color: #17324d;
            }

            [data-testid="stAlert"] p {
                color: #17324d !important;
            }

            .rail-card {
                max-width: 100%;
                overflow: hidden;
            }

            .reply-card {
                background: var(--panel-2);
                border-left: 3px solid var(--accent-2);
                border-radius: 6px;
                margin: 12px 0 0 18px;
                padding: 12px 14px;
            }

            .comment-meta {
                color: var(--muted);
                font-size: 13px;
                margin: 2px 0 8px;
            }

            @media (max-width: 760px) {
                .block-container {
                    padding: 1.2rem 1rem 3rem;
                }

                .masthead {
                    padding: 20px;
                }

                .masthead h1 {
                    font-size: 34px;
                }

                .dek,
                .article-body {
                    font-size: 16px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def article_by_id(article_id):
    """Returns one article by id."""
    return next(article for article in ARTICLES if article["id"] == article_id)


def section_articles(section):
    """Returns articles for a sidebar section."""
    if section == "Top Stories":
        return [article for article in ARTICLES if article["top_story"]]
    return [article for article in ARTICLES if article["section"] == section]


def saved_articles():
    """Returns saved articles."""
    return [article for article in ARTICLES if article["id"] in st.session_state.bookmarks]


def searched_articles(articles, query):
    """Filters articles by title, summary, body, section, and tags."""
    if not query.strip():
        return articles
    needle = query.strip().lower()
    matches = []
    for article in articles:
        haystack = " ".join(
            [
                article["title"],
                article["dek"],
                article["section"],
                article["author"],
                " ".join(article["tags"]),
                " ".join(article["summary"]),
                " ".join(article["body"]),
            ]
        ).lower()
        if needle in haystack:
            matches.append(article)
    return matches


def select_article(article_id):
    """Selects an article and opens the reader."""
    st.session_state.selected_article = article_id
    st.session_state.view = "Reader"
    rerun_app()


def rerun_app():
    """Reruns the app when the installed Streamlit version supports it."""
    if hasattr(st, "rerun"):
        st.rerun()
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def open_workspace(view):
    """Opens one workspace view."""
    st.session_state.view = view
    rerun_app()


def open_news_section(section):
    """Opens the feed for one news section."""
    st.session_state.selected_section = section
    st.session_state.view = "Feed"
    rerun_app()


def display_sidebar():
    """Displays navigation and filters."""
    with st.sidebar:
        st.title("NewsDesk")
        st.caption("News, briefs, and discussion.")

        selected_view = st.radio(
            "Workspace",
            VIEWS,
            index=VIEWS.index(st.session_state.view),
        )
        if selected_view != st.session_state.view:
            open_workspace(selected_view)

        selected_section = st.radio(
            "News sections",
            SECTIONS,
            index=SECTIONS.index(st.session_state.selected_section),
        )
        if selected_section != st.session_state.selected_section:
            open_news_section(selected_section)

        st.divider()
        st.metric("Total stories", len(ARTICLES))
        st.metric("Saved", len(st.session_state.bookmarks))
        comment_total = sum(
            len(comments) + sum(len(comment["replies"]) for comment in comments)
            for comments in st.session_state.comments_by_article.values()
        )
        st.metric("Reader comments", comment_total)
        st.markdown(
            "<p class='sidebar-credit'>Originally created through CodePath by the NewsDesk team.</p>",
            unsafe_allow_html=True,
        )


def display_top_bar():
    """Displays app-level context."""
    st.markdown(
        """
        <section class="masthead">
            <p class="brand-kicker">NewsDesk</p>
            <h1>Intelligent News Reader</h1>
            <p class="masthead-copy">
                Browse credible stories, read concise briefs, save coverage,
                and join the discussion from one focused newsroom workspace.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def display_feed_card(article, featured=False):
    """Displays one feed card."""
    with st.container(border=True):
        image_col, text_col = st.columns([1.15, 1.85], gap="medium")
        with image_col:
            st.markdown(
                f"<img class='feed-image' src='{article['image']}' alt='{article['title']}'>",
                unsafe_allow_html=True,
            )
        with text_col:
            st.markdown("<div class='feed-card-body'>", unsafe_allow_html=True)
            st.markdown(f"<p class='eyebrow'>{article['section']}</p>", unsafe_allow_html=True)
            if featured:
                st.subheader(article["title"])
            else:
                st.markdown(f"### {article['title']}")
            st.write(article["dek"])
            st.markdown(
                (
                    "<p class='story-meta'>"
                    f"{article['source']} | {article['author']} | "
                    f"{article['read_time']} | Trust {article['credibility']}%"
                    "</p>"
                ),
                unsafe_allow_html=True,
            )
            tag_line = "".join(f"<span class='tag'>{tag}</span>" for tag in article["tags"])
            st.markdown(tag_line, unsafe_allow_html=True)
            if st.button("Read article", key=f"read-{article['id']}", use_container_width=True):
                select_article(article["id"])
            st.markdown("</div>", unsafe_allow_html=True)


def display_feed():
    """Displays the commercial-style news feed."""
    display_top_bar()

    filter_col, sort_col = st.columns([2, 1])
    with filter_col:
        query = st.text_input("Search stories", placeholder="Search by topic, author, tag, or summary")
    with sort_col:
        sort = st.selectbox("Sort", ["Newest", "Highest trust", "Shortest read"])

    base_articles = section_articles(st.session_state.selected_section)
    articles = searched_articles(base_articles, query)
    if sort == "Highest trust":
        articles = sorted(articles, key=lambda item: item["credibility"], reverse=True)
    elif sort == "Shortest read":
        articles = sorted(articles, key=lambda item: int(item["read_time"].split()[0]))

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Section", st.session_state.selected_section)
    metric_col_2.metric("Stories shown", len(articles))
    metric_col_3.metric("Average trust", f"{round(sum(a['credibility'] for a in articles) / len(articles))}%" if articles else "N/A")

    if not articles:
        st.info("No stories match this filter yet.")
        return

    st.markdown("<div class='section-heading'><h2>Lead Story</h2></div>", unsafe_allow_html=True)
    display_feed_card(articles[0], featured=True)

    if len(articles) > 1:
        st.markdown("<div class='section-heading'><h2>More Coverage</h2></div>", unsafe_allow_html=True)
        for article in articles[1:]:
            display_feed_card(article)


def display_ai_summary(article):
    """Displays AI summary and a simple local question helper."""
    with st.container(border=True):
        st.subheader("AI Brief")
        st.caption("Generated reading brief")
        for item in article["summary"]:
            st.markdown(f"- {item}")

        question = st.text_input("Ask about this article", key=f"ask-{article['id']}", placeholder="Example: What is the main risk?")
        if question.strip():
            answer = ai_answer(article, question)
            st.info(answer)


def ai_answer(article, question):
    """Returns a lightweight local answer using article text."""
    question_words = {
        word.strip("?.!,;:").lower()
        for word in question.split()
        if len(word.strip("?.!,;:")) > 3
    }
    candidates = article["summary"] + article["body"]
    ranked = sorted(
        candidates,
        key=lambda text: len(
            question_words.intersection(
                {word.strip("?.!,;:").lower() for word in text.split()}
            )
        ),
        reverse=True,
    )
    return ranked[0] if ranked else article["summary"][0]


def display_poll(article):
    """Displays article usefulness poll."""
    with st.container(border=True):
        st.subheader("Usefulness Poll")
        poll = st.session_state.poll_by_article[article["id"]]
        vote = st.radio("Was this useful?", list(poll.keys()), key=f"poll-choice-{article['id']}")
        if st.button("Submit vote", key=f"vote-{article['id']}", use_container_width=True):
            record_vote(article["id"], vote)
            st.success("Vote recorded.")
            rerun_app()

        total = sum(poll.values())
        for label, count in poll.items():
            percent = count / total if total else 0
            st.caption(f"{label}: {count} votes ({percent:.0%})")
            st.progress(percent)


def display_reader_actions(article):
    """Displays reader actions."""
    is_saved = article["id"] in st.session_state.bookmarks
    col_1, col_2 = st.columns(2)
    with col_1:
        label = "Remove from saved" if is_saved else "Save article"
        if st.button(label, use_container_width=True):
            if is_saved:
                remove_saved_article(article["id"])
            else:
                save_article(article["id"])
            rerun_app()
    with col_2:
        if st.button("Back to feed", use_container_width=True):
            st.session_state.view = "Feed"
            rerun_app()


def display_article(article):
    """Displays the reader view."""
    st.markdown(f"<p class='eyebrow'>{article['section']}</p>", unsafe_allow_html=True)
    st.title(article["title"])
    st.markdown(f"<p class='dek'>{article['dek']}</p>", unsafe_allow_html=True)
    st.markdown(
        (
            "<p class='story-meta'>"
            f"{article['source']} | By {article['author']} | {article['published']} | "
            f"{article['read_time']} | Trust {article['credibility']}%"
            "</p>"
        ),
        unsafe_allow_html=True,
    )
    display_reader_actions(article)
    st.markdown(
        f"<img class='hero-image' src='{article['image']}' alt='{article['title']}'>",
        unsafe_allow_html=True,
    )
    tag_line = "".join(f"<span class='tag'>{tag}</span>" for tag in article["tags"])
    st.markdown(tag_line, unsafe_allow_html=True)
    st.divider()
    for paragraph in article["body"]:
        st.markdown(f"<p class='article-body'>{paragraph}</p>", unsafe_allow_html=True)


def display_related(article):
    """Displays related stories."""
    related = [
        item for item in ARTICLES
        if item["section"] == article["section"] and item["id"] != article["id"]
    ]
    if len(related) < 2:
        related.extend(
            item for item in ARTICLES
            if item["top_story"] and item["id"] != article["id"] and item not in related
        )
    related = related[:2]
    st.subheader("Related")
    for item in related:
        with st.container(border=True):
            st.markdown("<div class='rail-card'>", unsafe_allow_html=True)
            st.markdown(
                f"<img class='related-image' src='{item['image']}' alt='{item['title']}'>",
                unsafe_allow_html=True,
            )
            st.markdown(f"#### {item['title']}")
            st.markdown(
                f"<p class='story-meta'>{item['section']} | {item['read_time']}</p>",
                unsafe_allow_html=True,
            )
            if st.button("Open", key=f"related-{item['id']}", use_container_width=True):
                select_article(item["id"])
            st.markdown("</div>", unsafe_allow_html=True)


def display_comments(article):
    """Displays article discussion with replies."""
    comments = st.session_state.comments_by_article[article["id"]]
    st.subheader("Discussion")

    with st.form(f"comment-{article['id']}", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Your name")
        body = st.text_area("Comment", placeholder="Add a thoughtful response")
        submitted = st.form_submit_button("Post comment")
        if submitted and name.strip() and body.strip():
            add_comment(article["id"], name.strip(), body.strip())
            rerun_app()

    if not comments:
        st.info("No comments yet. Start the discussion.")

    for comment in comments:
        with st.container(border=True):
            st.markdown(f"**{comment['name']}**")
            st.caption(comment["time"])
            st.write(comment["body"])
            for reply in comment["replies"]:
                st.markdown(
                    f"""
                    <div class='reply-card'>
                        <strong>{escape(reply['name'])}</strong>
                        <div class='comment-meta'>{escape(reply['time'])}</div>
                        <p>{escape(reply['body'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.form(f"reply-{article['id']}-{comment['id']}", clear_on_submit=True):
                reply_name = st.text_input("Name", key=f"reply-name-{article['id']}-{comment['id']}", placeholder="Your name")
                reply_body = st.text_input("Reply", key=f"reply-body-{article['id']}-{comment['id']}", placeholder="Write a reply")
                reply_submitted = st.form_submit_button("Reply")
                if reply_submitted and reply_name.strip() and reply_body.strip():
                    add_reply(article["id"], comment["id"], reply_name.strip(), reply_body.strip())
                    rerun_app()


def display_reader():
    """Displays selected article plus right rail."""
    article = article_by_id(st.session_state.selected_article)
    main_col, rail_col = st.columns([1.9, 1], gap="medium")
    with main_col:
        display_article(article)
        st.divider()
        display_comments(article)
    with rail_col:
        display_ai_summary(article)
        st.write("")
        display_poll(article)
        st.write("")
        display_related(article)


def display_saved():
    """Displays saved article workspace."""
    display_top_bar()
    st.divider()
    saved = saved_articles()
    st.subheader("Saved Articles")
    if not saved:
        with st.container(border=True):
            st.markdown("### Your reading list is empty")
            st.write("Open a story in the Reader workspace and use **Save article** to keep it here.")
            if st.button("Browse top stories", use_container_width=True):
                st.session_state.view = "Feed"
                st.session_state.selected_section = "Top Stories"
                rerun_app()
        return
    for article in saved:
        display_feed_card(article)


def display_about():
    """Displays public product context."""
    st.markdown("<p class='brand-kicker'>About NewsDesk</p>", unsafe_allow_html=True)
    st.title("Built From a Team Newsroom Project")
    st.write(
        "NewsDesk started as a CodePath group project and has been refined into "
        "a cleaner news-reader experience with focused browsing, article briefs, "
        "saved stories, reader polls, and discussion."
    )

    overview_col, team_col = st.columns([1.2, 1], gap="large")
    with overview_col:
        with st.container(border=True):
            st.subheader("Reader Experience")
            st.write(
                "Browse section-based coverage, open a focused reader view, "
                "review quick article briefs, save stories, vote on usefulness, "
                "and participate in threaded discussions."
            )

    with team_col:
        with st.container(border=True):
            st.subheader("Original Contributors")
            st.write("Created through CodePath by:")
            st.markdown("- Leanelys Gonzalez")
            st.markdown("- Jermaine Adesanya")
            st.markdown("- Evan Morales")
            st.markdown("- Dipendra Pandey")
            st.markdown("- Anthony Torres")

    st.divider()
    if st.button("Open news feed", use_container_width=True):
        st.session_state.view = "Feed"
        rerun_app()


def display_app_page():
    """Displays the app."""
    st.set_page_config(
        page_title="NewsDesk",
        page_icon=":newspaper:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_state()
    inject_styles()
    display_sidebar()

    if st.session_state.view == "Reader":
        display_reader()
    elif st.session_state.view == "Saved":
        display_saved()
    elif st.session_state.view == "About":
        display_about()
    else:
        display_feed()


if __name__ == "__main__":
    display_app_page()
