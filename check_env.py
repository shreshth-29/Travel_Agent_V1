# check_env.py
# Checks that the expected API keys are present in .env (or the environment).
# Prints only the first 4 characters of each value.

import os

from settings import load_env

EXPECTED_KEYS = ["GOOGLE_API_KEY", "SERPER_API_KEY", "FIRECRAWL_API_KEY", "GROQ_API_KEY"]


def main() -> None:
    load_env()
    missing = []
    for key in EXPECTED_KEYS:
        value = os.getenv(key)
        if value:
            print(f"{key}: found ({value[:4]}...)")
        else:
            print(f"{key}: missing")
            missing.append(key)
    if missing:
        print("\nMissing keys. Copy .env.example to .env and fill them in.")
    else:
        print("\nAll expected keys found.")


if __name__ == "__main__":
    main()
