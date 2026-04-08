import asyncio
import os
from typing import List
from openai import OpenAI
from env import MyEnvV4Env
from models import MyEnvV4Action

# Environment Configuration
# FIX: Point directly to Google's OpenAI-compatible endpoint for Gemini models
API_BASE_URL = os.getenv("API_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
# FIX: Use Gemini API Key instead of Hugging Face token
API_KEY = os.getenv("GEMINI_API_KEY") or ""
MODEL_NAME = "gemini-2.0-flash"
TASK_NAME = "security-mail-triage"

SYSTEM_PROMPT = """
You are an Advanced Email Security Agent. Analyze the metadata (headers, SPF/DKIM), URLs, and content.
Categories:
- INBOX: Trusted academic/official domains, passed auth, clean history.
- SPAM: Mass marketing, generic lottery/sales, usually safe but unwanted.
- QUARANTINE: Phishing, spear-phishing, credential theft, high-urgency threats, typo-squatted domains.

Rules:
1. Examine 'raw_headers' and 'auth_results'.
2. Inspect 'urls' for low reputation or high age.
3. Provide reasoning first, then your decision.

Respond in JSON format:
{
  "reasoning": "Explain your logic here...",
  "message": "INBOX|SPAM|QUARANTINE"
}
"""


async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = MyEnvV4Env()

    rewards = []
    print(f"[START] Testing Security Triage Environment...")

    result = await env.reset()
    step_idx = 1

    while not result.done:
        obs = result.observation
        prompt = f"Sender: {obs.sender}\nSubject: {obs.subject}\nBody: {obs.body}\nHeaders: {obs.raw_headers}\nURLs: {obs.urls}"

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            import json
            data = json.loads(response.choices[0].message.content)

            action = MyEnvV4Action(message=data["message"], reasoning=data["reasoning"])
            result = await env.step(action)
            rewards.append(result.reward)

            print(f"[STEP {step_idx}] Action: {action.message} | Reward: {result.reward:.2f}")
            step_idx += 1

            # Prevent hitting Gemini Free Tier rate limits (15 requests per minute & token limits)
            # Increased to 10 seconds to ensure we do not hit the burst quotas.
            await asyncio.sleep(10)
        except Exception as e:
            print(f"[ERROR] Step {step_idx}: {e}")
            break

    score = sum(rewards) / len(rewards) if rewards else 0
    print(f"[END] Final Score: {score:.3f}")


if __name__ == "__main__":
    asyncio.run(main())