import asyncio
import random
from typing import Optional, List, Dict, Any
from types import SimpleNamespace
from fastapi import FastAPI, Body
from openenv.core.env_server import Environment
from models import MyEnvV4Observation, MyEnvV4Action, URLInfo


class MyEnvV4Env(Environment):
    def __init__(self):
        super().__init__()
        self.dataset = self._generate_sophisticated_dataset()
        self.current_step = 0

    def _generate_sophisticated_dataset(self):
        """
        Expanded dataset with 15 samples across 3 difficulty levels.
        """
        base_data = [
            # LEVEL 1: CLEAR CASES
            {
                "sender": "registrar@manipal.edu",
                "subject": "Semester Registration Open",
                "body": "Dear student, please register for the Fall semester via the student portal.",
                "raw_headers": "Received: from mail.manipal.edu (14.139.161.20) by mx.google.com; SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [],
                "label": "INBOX",
                "difficulty": 1
            },
            {
                "sender": "no-reply@amazon.com",
                "subject": "Your Order #123-4567 has shipped",
                "body": "Track your package delivery status in your Amazon account.",
                "raw_headers": "Received: from a9-12.smtp-out.amazonses.com... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [
                    {"url": "https://amazon.com/track", "is_shortened": False, "domain_age_days": 8000, "has_ssl": True,
                     "reputation_score": 1.0}],
                "label": "INBOX",
                "difficulty": 1
            },
            {
                "sender": "win-money@lottery-global.net",
                "subject": "YOU WON!! $1,000,000",
                "body": "Congratulations! You have been selected as our winner. CLAIM YOUR $1M NOW!",
                "raw_headers": "Received: from unknown-relay.co (103.22.1.5)... SPF: none; DKIM: fail;",
                "auth_results": {"SPF": "none", "DKIM": "fail", "DMARC": "none"},
                "urls": [{"url": "http://get-cash-free.net/claim", "is_shortened": False, "domain_age_days": 2,
                          "has_ssl": False, "reputation_score": 0.1}],
                "label": "SPAM",
                "difficulty": 1
            },
            {
                "sender": "viagra-sales@pharma-dealz.biz",
                "subject": "Cheapest Meds Online",
                "body": "Buy now and save 90% on all prescription drugs. No prescription needed!",
                "raw_headers": "Received: from botnet-node.ru... SPF: softfail;",
                "auth_results": {"SPF": "softfail", "DKIM": "none", "DMARC": "none"},
                "urls": [{"url": "http://cheap-rx.biz", "is_shortened": False, "domain_age_days": 15, "has_ssl": False,
                          "reputation_score": 0.05}],
                "label": "SPAM",
                "difficulty": 1
            },
            {
                "sender": "support@netflix-security.com",
                "subject": "Update Payment Method",
                "body": "Your Netflix subscription has expired. Click here to login and update billing.",
                "raw_headers": "Received: from suspicious-vps.com... SPF: fail; DMARC: fail;",
                "auth_results": {"SPF": "fail", "DKIM": "none", "DMARC": "fail"},
                "urls": [{"url": "https://bit.ly/fake-netflix-login", "is_shortened": True, "domain_age_days": 3,
                          "has_ssl": True, "reputation_score": 0.02}],
                "label": "QUARANTINE",
                "difficulty": 1
            },
            # LEVEL 2: NUANCED
            {
                "sender": "news@internshala-mail.com",
                "subject": "New Internships in Manipal",
                "body": "Check out these new opportunities for CSE students. Apply today!",
                "raw_headers": "Received: from mktg.server.com... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [{"url": "https://internshala.com/n/123", "is_shortened": False, "domain_age_days": 2500,
                          "has_ssl": True, "reputation_score": 0.95}],
                "label": "SPAM",
                "difficulty": 2
            },
            {
                "sender": "marketing@swiggy.in",
                "subject": "50% OFF your next meal!",
                "body": "Hungry? Use code HUNGRY50 at checkout.",
                "raw_headers": "Received: from swiggy-mail.in... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [],
                "label": "SPAM",
                "difficulty": 2
            },
            {
                "sender": "hr@startup-hiring.co",
                "subject": "Interview Invitation",
                "body": "We saw your profile on LinkedIn and want to chat about a role.",
                "raw_headers": "Received: from linkedin-referral.com... SPF: neutral;",
                "auth_results": {"SPF": "neutral", "DKIM": "none", "DMARC": "none"},
                "urls": [{"url": "https://startup-hiring.co/apply", "is_shortened": False, "domain_age_days": 45,
                          "has_ssl": True, "reputation_score": 0.6}],
                "label": "INBOX",
                "difficulty": 2
            },
            {
                "sender": "alert@banking-secure.net",
                "subject": "Suspicious Activity Detected",
                "body": "We detected an unusual login to your account from Russia. Please verify.",
                "raw_headers": "Received: from spoofed-host.com... SPF: softfail; DMARC: none;",
                "auth_results": {"SPF": "softfail", "DKIM": "none", "DMARC": "none"},
                "urls": [{"url": "https://t.co/secure-bank-login", "is_shortened": True, "domain_age_days": 10,
                          "has_ssl": True, "reputation_score": 0.3}],
                "label": "QUARANTINE",
                "difficulty": 2
            },
            {
                "sender": "noreply@github.com",
                "subject": "[GitHub] A personal access token has been added",
                "body": "A new personal access token was added to your account. If this wasn't you, click here.",
                "raw_headers": "Received: from out-21.smtp.github.com... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [{"url": "https://github.com/settings/tokens", "is_shortened": False, "domain_age_days": 6000,
                          "has_ssl": True, "reputation_score": 1.0}],
                "label": "INBOX",
                "difficulty": 2
            },
            # LEVEL 3: SPEAR PHISHING
            {
                "sender": "dean.office@manipal-edu.in",
                "subject": "Urgent: Faculty Grievance Report",
                "body": "A report has been filed against your department. Review the grievances here immediately.",
                "raw_headers": "Received: from rogue-vps.xyz... SPF: fail; DMARC: fail;",
                "auth_results": {"SPF": "fail", "DKIM": "none", "DMARC": "fail"},
                "urls": [{"url": "https://bit.ly/3xYz1-grievance", "is_shortened": True, "domain_age_days": 5,
                          "has_ssl": True, "reputation_score": 0.05}],
                "label": "QUARANTINE",
                "difficulty": 3
            },
            {
                "sender": "it-support@manipal-helpdesk.com",
                "subject": "Mandatory Password Reset",
                "body": "As per the new MIT security policy, all students must reset their password today.",
                "raw_headers": "Received: from mail-delivery.online... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "none"},
                "urls": [{"url": "http://manipal-helpdesk.com/reset", "is_shortened": False, "domain_age_days": 1,
                          "has_ssl": False, "reputation_score": 0.1}],
                "label": "QUARANTINE",
                "difficulty": 3
            },
            {
                "sender": "prof.sharma@mit-manipal.org",
                "subject": "Final Exam Paper Leak?",
                "body": "I suspect the paper has leaked. Look at this screenshot.",
                "raw_headers": "Received: from sendgrid.net... SPF: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "none", "DMARC": "none"},
                "urls": [{"url": "https://dropbox-files.com/s/xyz", "is_shortened": False, "domain_age_days": 4,
                          "has_ssl": True, "reputation_score": 0.2}],
                "label": "QUARANTINE",
                "difficulty": 3
            },
            {
                "sender": "accounts@google-security.info",
                "subject": "Critical Security Alert",
                "body": "Someone just used your password to try to sign in.",
                "raw_headers": "Received: from host-12.xyz... SPF: fail;",
                "auth_results": {"SPF": "fail", "DKIM": "none", "DMARC": "fail"},
                "urls": [{"url": "https://google-secure-login.info", "is_shortened": False, "domain_age_days": 2,
                          "has_ssl": True, "reputation_score": 0.01}],
                "label": "QUARANTINE",
                "difficulty": 3
            },
            {
                "sender": "library@manipal.edu",
                "subject": "Overdue Book Notice",
                "body": "Your copy of 'Computer Networks' is overdue.",
                "raw_headers": "Received: from mail.manipal.edu... SPF: pass; DKIM: pass;",
                "auth_results": {"SPF": "pass", "DKIM": "pass", "DMARC": "pass"},
                "urls": [{"url": "https://portal.manipal.edu/pay", "is_shortened": False, "domain_age_days": 4000,
                          "has_ssl": True, "reputation_score": 1.0}],
                "label": "INBOX",
                "difficulty": 3
            }
        ]
        return base_data

    async def reset(self):
        self.current_step = 0
        return self._get_result()

    def _get_result(self, reward=0.0, done=False):
        if self.current_step >= len(self.dataset):
            obs = MyEnvV4Observation(
                sender="N/A", subject="N/A", body="N/A", raw_headers="",
                hop_count=0, auth_results={}, urls=[], echoed_message="End of Session"
            )
            return SimpleNamespace(observation=obs, reward=reward, done=True)

        data = self.dataset[self.current_step]
        obs = MyEnvV4Observation(
            sender=data["sender"],
            subject=data["subject"],
            body=data["body"],
            raw_headers=data["raw_headers"],
            hop_count=data["raw_headers"].count("Received:"),
            auth_results=data["auth_results"],
            urls=[URLInfo(**u) for u in data["urls"]],
            echoed_message=f"Task {self.current_step + 1}/{len(self.dataset)}"
        )
        return SimpleNamespace(observation=obs, reward=reward, done=done)

    async def step(self, action: MyEnvV4Action):
        if self.current_step >= len(self.dataset):
            return self._get_result(done=True)

        target = self.dataset[self.current_step]
        correct = target["label"]
        prediction = action.message.strip().upper()

        reward = 0.0
        if prediction == correct:
            reward = 1.0 + (target["difficulty"] * 0.1)
        elif correct in ["SPAM", "QUARANTINE"] and prediction in ["SPAM", "QUARANTINE"]:
            reward = 0.4
        elif correct == "QUARANTINE" and prediction == "INBOX":
            reward = -1.5
        elif correct == "INBOX" and prediction == "QUARANTINE":
            reward = -0.5

        if hasattr(action, 'reasoning') and action.reasoning and len(action.reasoning) > 30:
            reward += 0.05

        final_reward = max(0.0, min(1.0, reward))
        self.current_step += 1
        done = self.current_step >= len(self.dataset)

        return self._get_result(reward=final_reward, done=done)

    async def state(self):
        return {"current_step": self.current_step, "total_tasks": len(self.dataset)}


# Global instance
my_env = MyEnvV4Env()
app = FastAPI()


@app.post("/reset")  # FIXED: Must be POST for OpenEnv validators
async def reset(payload: Dict[Any, Any] = Body(default={})):
    res = await my_env.reset()
    return {"observation": res.observation, "reward": res.reward, "done": res.done}


@app.post("/step")
async def step(action: MyEnvV4Action):
    res = await my_env.step(action)
    return {"observation": res.observation, "reward": res.reward, "done": res.done}


@app.get("/state")
async def state():
    return await my_env.state()