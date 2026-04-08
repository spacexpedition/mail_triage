import asyncio
import os
import json
from openai import OpenAI
from env import MyEnvV4Env
from models import MyEnvV4Action

# Environment Configuration
# Standard OpenEnv evaluation environments inject these env vars
API_BASE_URL = os.getenv("API_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
MODEL_NAME = "gemini-2.0-flash"

SYSTEM_PROMPT = """
You are an Advanced Email Security Agent. Analyze the metadata, URLs, and content.
Categories:
- INBOX: Trusted academic/official domains, passed auth.
- SPAM: Unwanted marketing or sales.
- QUARANTINE: Phishing, typo-squatting, or high-risk threats.

Respond in strict JSON:
{
  "reasoning": "Explain your logic...",
  "message": "INBOX|SPAM|QUARANTINE"
}
"""


async def main():
    if not API_KEY:
        print("[ERROR] No API key found. Please set GEMINI_API_KEY.")
        return

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = MyEnvV4Env()

    rewards = []
    print(f"[START] Running Security Triage Evaluation...")

    # OpenEnv Reset
    result = await env.reset()
    step_idx = 1

    while not result.done:
        obs = result.observation
        # Prepare the prompt by dumping complex URL objects to dictionaries
        prompt = (
            f"Sender: {obs.sender}\n"
            f"Subject: {obs.subject}\n"
            f"Body: {obs.body}\n"
            f"Headers: {obs.raw_headers}\n"
            f"Auth: {obs.auth_results}\n"
            f"URLs: {[u.model_dump() for u in obs.urls]}"
        )

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            # Create action and step the environment
            action = MyEnvV4Action(message=data["message"], reasoning=data["reasoning"])
            result = await env.step(action)
            rewards.append(result.reward)

            print(f"[STEP {step_idx}] Result: {action.message} | Reward: {result.reward:.2f}")
            step_idx += 1

            # Sleep to respect rate limits (Gemini 2.0 Flash)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Step {step_idx}: {e}")
            break

    final_score = sum(rewards) / len(rewards) if rewards else 0
    print(f"[END] Evaluation Complete. Final Score: {final_score:.3f}")


if __name__ == "__main__":
    asyncio.run(main())