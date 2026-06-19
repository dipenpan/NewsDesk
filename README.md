# NewsDesk

[Live App](https://newsdesk.streamlit.app/) | [Repository](https://github.com/dipenpan/NewsDesk)

NewsDesk is a Streamlit news reader built for browsing curated stories, reading concise article briefs, saving coverage, voting on usefulness, and joining threaded discussions.

The project began as a CodePath group project and has been refined into a polished reader experience with cleaner navigation, improved styling, and persistent feedback features.

## Features

- Section-based news feed for Top Stories, Technology, Health, and Education
- Search and sorting tools for quickly finding relevant coverage
- Focused reader view with article metadata, source, tags, trust score, and related stories
- AI-style brief panel with concise summary bullets and a local article question helper
- Usefulness poll with live vote percentages
- Saved stories view for later reading
- Threaded comments and replies
- Runtime SQLite storage for saved stories, votes, comments, and replies

## Live Demo

Open the deployed app:

```text
https://newsdesk.streamlit.app/
```

## Tech Stack

- Python
- Streamlit
- SQLite
- HTML/CSS styling inside Streamlit

## Original Contributors

NewsDesk was originally created through CodePath by:

- Leanelys Gonzalez
- Jermaine Adesanya
- Evan Morales
- Dipendra Pandey
- Anthony Torres

## Project Structure

```text
.
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/config.toml    # Streamlit configuration
├── Dockerfile                # Optional container build file
├── LICENSE
└── README.md
```

## Run Locally

Clone the repository:

```shell
git clone https://github.com/dipenpan/NewsDesk.git
cd NewsDesk
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Start the app:

```shell
streamlit run app.py
```

By default, Streamlit opens at:

```text
http://localhost:8501
```

## Data Storage

NewsDesk creates a local SQLite database at runtime for saved stories, poll votes, comments, and replies.

On Streamlit Community Cloud, runtime storage is temporary and may reset when the app restarts. For durable multi-user storage, replace the runtime SQLite database with a hosted database such as PostgreSQL, Supabase, Firebase, or Cloud SQL.

## Verification

Run a syntax check:

```shell
python -c "compile(open('app.py', encoding='utf-8').read(), 'app.py', 'exec')"
```

## License

This project is licensed under the MIT License.
