"""
LLM Client Wrapper for CareerCompass
SIH25094 - CSE473 Agentic AI

Supports Gemini API (primary), OpenAI API (secondary),
and an intelligent, deterministic, dataset-grounded fallback mode
if no API keys are supplied or if rate limits occur.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.preferred_provider = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()
        self.active_mode = "fallback"
        self._init_clients()

    def _init_clients(self):
        # 1. Try Gemini
        if self.gemini_key and self.gemini_key != "your_gemini_api_key_here":
            try:
                # Try google.genai first
                from google import genai
                self.gemini_client = genai.Client(api_key=self.gemini_key)
                self.active_mode = "gemini_genai"
                logger.info("Initialized Google GenAI client.")
                return
            except Exception as e:
                try:
                    import google.generativeai as gai
                    gai.configure(api_key=self.gemini_key)
                    self.gemini_model = gai.GenerativeModel("gemini-1.5-flash")
                    self.active_mode = "gemini_legacy"
                    logger.info("Initialized Google GenerativeAI (legacy) client.")
                    return
                except Exception as ex:
                    logger.warning(f"Could not initialize Gemini: {ex}")

        # 2. Try OpenAI
        if self.openai_key and self.openai_key != "your_openai_api_key_here":
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.openai_key)
                self.active_mode = "openai"
                logger.info("Initialized OpenAI client.")
                return
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI: {e}")

        # 3. Autonomous Fallback Engine
        self.active_mode = "fallback"
        logger.info("Operating in Autonomous O*NET Dataset-Driven Fallback Mode.")

    def generate_json_response(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Attempts to call active LLM provider. Returns parsed JSON dict or None.
        """
        if self.active_mode == "fallback":
            return None

        # Try Gemini GenAI
        if self.active_mode == "gemini_genai":
            try:
                prompt_full = f"{system_prompt}\n\nPlease respond ONLY with valid JSON.\n\n{user_prompt}"
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_full,
                )
                text = response.text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text)
            except Exception as e:
                logger.warning(f"Gemini GenAI generation failed: {e}. Falling back.")
                return None

        # Try Gemini Legacy
        if self.active_mode == "gemini_legacy":
            try:
                prompt_full = f"{system_prompt}\n\nPlease respond ONLY with valid JSON.\n\n{user_prompt}"
                response = self.gemini_model.generate_content(prompt_full)
                text = response.text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text)
            except Exception as e:
                logger.warning(f"Gemini Legacy generation failed: {e}. Falling back.")
                return None

        # Try OpenAI
        if self.active_mode == "openai":
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt + " Respond ONLY in JSON."},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}. Falling back.")
                return None

        return None

    def chat_reply(self, messages: list, context_str: str = "") -> str:
        """
        Chat completion for the AI Career Chatbot page.
        """
        system_instruction = (
            "You are CareerCompass AI, an expert career counselor and academic mentor. "
            "You advise students with factual guidance grounded in O*NET occupational benchmarks. "
            "Always be encouraging, actionable, structured, and realistic.\n\n"
            f"STUDENT CONTEXT:\n{context_str}"
        )

        if self.active_mode == "gemini_genai":
            try:
                full_conv = f"SYSTEM INSTRUCTION: {system_instruction}\n\n"
                for m in messages:
                    full_conv += f"{m['role'].upper()}: {m['content']}\n"
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_conv
                )
                return response.text
            except Exception as e:
                logger.warning(f"Gemini chat failed: {e}")

        elif self.active_mode == "gemini_legacy":
            try:
                full_conv = f"SYSTEM INSTRUCTION: {system_instruction}\n\n"
                for m in messages:
                    full_conv += f"{m['role'].upper()}: {m['content']}\n"
                response = self.gemini_model.generate_content(full_conv)
                return response.text
            except Exception as e:
                logger.warning(f"Gemini legacy chat failed: {e}")

        elif self.active_mode == "openai":
            try:
                chat_msgs = [{"role": "system", "content": system_instruction}] + messages
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=chat_msgs
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"OpenAI chat failed: {e}")

        # Deterministic Grounded Fallback Chatbot
        last_query = messages[-1]["content"].lower() if messages else ""
        if "project" in last_query:
            return (
                "For your targeted career path, high-impact projects are key. "
                "I recommend building an end-to-end portfolio project featuring:\n"
                "1. Clean modular Python code with unit tests.\n"
                "2. Real-world dataset integration (e.g., Kaggle or public APIs).\n"
                "3. A live interactive deployment (Streamlit or Docker container).\n"
                "4. A well-documented GitHub repository with an architecture diagram and README."
            )
        elif "interview" in last_query or "resume" in last_query:
            return (
                "To prepare for technical interviews and placement drives:\n"
                "• Master Core Data Structures & Algorithms (Arrays, Hash Maps, Trees, Graphs).\n"
                "• Practice LeetCode Easy & Medium problems consistently (3-4 problems/week).\n"
                "• Prepare STAR-method stories for behavioral questions.\n"
                "• Ensure your resume highlights measurable metrics (e.g. 'Reduced latency by 35%')."
            )
        elif "course" in last_query or "learn" in last_query:
            return (
                "Based on your profile, prioritize high-relevance courses:\n"
                "• Focus first on mastering fundamentals before moving to complex frameworks.\n"
                "• Check out the verified courses recommended in your Learning Roadmap.\n"
                "• Complement video courses with official documentation and hands-on coding."
            )
        else:
            return (
                "Based on your student profile and O*NET benchmarks, staying consistent with your "
                "5-phase roadmap is the fastest route to industry readiness. Focus on closing your "
                "high-priority skill gaps and practicing hands-on problem solving every week!"
            )
