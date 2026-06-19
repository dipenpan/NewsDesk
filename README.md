# NewsDesk

NewsDesk is a Streamlit news reader for browsing section-based coverage, opening focused article pages, saving stories, voting on article usefulness, and joining threaded discussions.

The app began as a CodePath group project and has been refined into a cleaner reader experience with stronger navigation, polished styling, and local persistence for saved content and feedback.

## Features

- Section-based feed for Top Stories, Technology, Health, and Education
- Search and sorting controls for quickly finding relevant stories
- Focused reader view with article metadata, tags, trust score, and related stories
- AI Brief panel with concise bullet summaries and a local article question helper
- Usefulness poll with live vote percentages
- Saved articles list for later reading
- Threaded comments and replies
- SQLite persistence for saved stories, votes, comments, and replies

## Original Contributors

NewsDesk was originally created through CodePath by:

- Leanelys Gonzalez
- Jermaine Adesanya
- Evan Morales
- Dipendra Pandey
- Anthony Torres

## Tech Stack

- Python
- Streamlit
- SQLite

## Project Structure

```text
.
├── app.py                         # Main Streamlit app
├── requirements.txt               # Python dependencies
├── .streamlit/config.toml         # Streamlit server config
├── Dockerfile                     # Container build config
├── LICENSE
└── README.md
```

## Run Locally

Install dependencies:

```shell
pip install -r requirements.txt
```

Start the app:

```shell
streamlit run app.py
```

Streamlit will print the local URL after startup. By default, open:

```text
http://localhost:8501
```

## Data Storage

NewsDesk stores saved articles, poll votes, comments, and replies in a local SQLite database created at runtime. On hosted environments such as Streamlit Community Cloud, this storage is temporary and can reset when the app restarts.

For durable multi-user storage, replace the runtime SQLite database with a hosted database such as PostgreSQL, Supabase, Firebase, or Cloud SQL.

## Verification

Run syntax checks:

```shell
python -c "compile(open('app.py', encoding='utf-8').read(), 'app.py', 'exec')"
```
