# Overview

This is a quick script using Spacy, Supabase, and PRAW to parse stories and add them to a PSQL database.

## Installation

```
git clone https://github.com/lukeweston1234/geostory_refactor_api.git
cd geostory_refactor_api
touch .env
python -m spacy download en_core_web_md
pip install -r ./requirements.txt
```

Set the following environment variables in a .env file. The first five are for PRAW
```
USERNAME=""
PASSWORD=""
CLIENT_SECRET=""
CLIENT_ID=""
USER_AGENT=""
SUPABASE_URL=""
SUPABASE_KEY=""
```

Running executable
```
python3 main.py
```