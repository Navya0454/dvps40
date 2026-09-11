from pathlib import Path
from dotenv import dotenv_values
from groq import Groq

# Find the .env file in the same folder as this Python file
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Read variables directly from .env
config = dotenv_values(ENV_FILE)

# Get Groq API token
GROQ_API_KEY = config.get("GROQ_API_TOKEN")

if not GROQ_API_KEY:
    raise RuntimeError(
        f"GROQ_API_TOKEN is missing from .env\n"
        f"Expected location: {ENV_FILE}"
    )

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


def diagnose_with_groq(error_message):

    prompt = f"""
You are DVPS40, an autonomous DevOps troubleshooting AI.

Analyze the following deployment/server error:

ERROR:
{error_message}

Provide the response in exactly this structure:

Error Type:
Root Cause:
Severity:
Recommended Fix:
Exact Commands/Code Changes:

Keep the answer practical, concise, and suitable for a developer.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def generate_fix(error_message, diagnosis):

    prompt = f"""
You are DVPS40, an autonomous DevOps auto-fix engine.

You are given a deployment/server error and an AI diagnosis.

ERROR:
{error_message}

DIAGNOSIS:
{diagnosis}

Generate the safest practical fix for this problem.

Return the response in exactly this structure:

Fix Type:
Package/File:
Fix Command:
Code Change:
Verification Command:
Risk Level:

Rules:
- Do not invent files or packages.
- Prefer the smallest possible fix.
- If a Python package is missing, recommend installing that package.
- If a code change is required, show the exact change.
- Do not execute anything.
- Keep the fix concise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content