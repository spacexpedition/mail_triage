---
title: Mail Triage Agent
emoji: 👀
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 8000
---
Mail Triage Agent v4 (Security Evaluation)

This repository contains a high-fidelity environment and an autonomous agent designed for Email Security Triage. The project focuses on detecting sophisticated threats like "Digital Seduction" (Phishing), typo-squatted domains, and malicious URL redirections.

🚀 Overview

The system consists of two primary components:

Environment (env.py): A FastAPI-based server implementing the OpenEnv specification. it serves a dataset of 15 email scenarios categorized by difficulty (1 to 3).

Agent Logic (inference.py): An LLM-powered agent (using gemini-2.0-flash) that analyzes email metadata, headers, and URLs to make triage decisions.

🛠 Project Structure

env.py: The core environment logic. Includes the dataset and scoring metrics.

inference.py: The agent's decision-making loop.

models.py: Pydantic models defining the Observation and Action spaces.

openenv.yaml: Metadata for the OpenEnv benchmark framework.

Dockerfile: Containerization setup for deployment.

requirements.txt: Python dependencies.

🧪 Scoring Logic

The environment uses a sophisticated reward system:

Perfect Classification: 1.0 + (difficulty * 0.1)

Partial Credit: 0.4 (e.g., classifying Phishing as Spam).

Dangerous Failure: -1.5 (e.g., letting Phishing into the INBOX).

False Positive: -0.5 (e.g., blocking legitimate mail).

Reasoning Bonus: +0.05 for providing detailed justifications.

⚙️ Setup & Installation

Prerequisites

Docker (optional)

Python 3.10+

A Google Gemini API Key

Local Execution

Install dependencies:

pip install -r requirements.txt


Set your environment variables:

export GEMINI_API_KEY="your_api_key_here"


Run the environment server:

uvicorn env:app --host 0.0.0.0 --port 8000


In a separate terminal, run the agent:

python inference.py


🛡 Security Scenarios Covered

Clean: Official Manipal or Amazon communications with valid SPF/DKIM.

Spam: Marketing mail from Swiggy or Internshala.

Phishing: Typo-squatted domains (e.g., manipal-edu.in vs manipal.edu) and shortened URLs.

Credential Theft: Fake security alerts from bank/Google look-alikes.

