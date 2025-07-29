# test_env.py
# This script tests if environment variables are read correctly from a .env file.

import os
from dotenv import load_dotenv

def test_env_variables(env_file_name="travelagent.env"):
    """
    Loads environment variables from the specified .env file and prints their values.
    """
    print(f"Attempting to load environment variables from {env_file_name}...")

    # Load environment variables from the specified .env file
    # This will look for the file in the current directory by default.
    load_dotenv(dotenv_path=env_file_name)

    # List of API keys you expect to find in your .env file
    # You can add or remove keys based on what you have in your travelegent.env
    api_keys = [
        "SERPER_API_KEY",
        "FIRECRAWL_API_KEY",
        "GROQ_API_KEY",
        "GOOGLE_API_KEY"
    ]

    all_keys_found = True
    for key in api_keys:
        value = os.getenv(key)
        if value:
            print(f"'{key}' found: {value[:5]}... (first 5 chars)") # Print first 5 chars for security
        else:
            print(f"WARNING: '{key}' not found or is empty in {env_file_name}")
            all_keys_found = False

    if all_keys_found:
        print("\nAll expected API keys were found and read successfully!")
    else:
        print("\nSome expected API keys were missing or empty. Please check your .env file.")

if __name__ == "__main__":
    # Ensure your 'travelegent.env' file is in the same directory as this script,
    # or provide the full path to it.
    test_env_variables()
