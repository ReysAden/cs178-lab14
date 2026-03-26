# CS 178 — Lab 14 Starter Repo
# Reys Aden

This is the starter repository for **Lab 14: Flask Part II**.

## Setup

1. **Fork** this repo to your own GitHub account
2. Clone your fork to your local machine
3. Download `creds.py` from Blackboard and place it in this folder
4. Make sure your GitHub Actions secrets are still set from Lab 9:
   - `EC2_HOST`
   - `EC2_USER`
   - `EC2_PRIVATE_KEY`

## Repo Structure

```
lab14-starter/
├── flaskapp.py          # Main Flask app — add your routes here
├── dbTesting.py         # Test your database connection here
├── creds_sample.py      # Shows the expected format for creds.py
├── requirements.txt     # Python dependencies (installed automatically on EC2)
├── templates/
│   └── textbox.html     # HTML form template (you'll build this in Section 3)
└── .github/
    └── workflows/
        └── deploy.yml   # Auto-deploys to EC2 on every push to main
```

## Important

- `creds.py` is listed in `.gitignore` — never push it to GitHub
- Every `git push` to `main` will automatically deploy to your EC2 instance
