
from __future__ import annotations  # Tells Python: "Don't panic if you see a name I haven't defined yet"

import argparse     # Lets the user choose a platform from your list
import os           # To talk to your computer's operating system
import sys  # Controls how your code starts, runs, and stops
from pathlib import Path  # To manage folder and file paths easily

# LangChain: The main framework to connect AI models with logic
from langchain_core.prompts import PromptTemplate      # A "Form" for your instructions

# Google GenAI: The specific bridge to use Google's Gemini AI
from langchain_google_genai import ChatGoogleGenerativeAI

# Dotenv: Loads secret API keys from a private .env file
from dotenv import load_dotenv

PLATFORMS = ("Meta", "Instagram", "LinkedIn", "Youtube")

def _platform_prompt(platform: str) -> PromptTemplate:
   platform = platform.strip()  # Remove extra spaces from the text

   if platform not in PLATFORMS: # raise stop code right now
    raise ValueError(f"Unsupported platform '{platform}'. Choose one of: {','.join(PLATFORMS)}") 
   
  # Rules Folder: A list of specific instructions for each social media site
   templates: dict[str,str] = {
     "Meta":(
       "You are a social media copywriter.\n"
       "Write a Meta(Facebook) post about: {topic}\n\n"
       "Tone: friendly, community-first, conversational.\n"
       "Format requirements:\n"
       "- 1 hook line\n"
       "- 2-4 short paragraphs (easy to read on mobile)\n"
       "- 1 clear call-to-action question at the end\n"
       "- 0-3 relevant emojis(not excessive)"
       "- No hashtags (or at most 1 subtle hashtag)\n"
     ),
     "Instagram":(
       "You are an Instagram content creator.\n"
       "Create an Instagram caption about: {topic}\n\n"
       "Tone: energetic,punchy, modern.\n"
       "Format requirements: \n"
       "- Start with a strong hook (first line)\n"
       "- 1 short story or tip list (2-s bullets max)\n"
       "- Include a clear CTA (save/share/comment)\n"
       "- Add 8-15 relevant hashtags at the end on a new line\n"
       "-Keep total length under 1200 characters\n"
     ),
     "LinkedIn": (
       "You are a professional Linkedin ghostwriter"
       "Write a LinkedIn post about: {topic}\n\n"
       "Tone: professional, insightful, credible (no hype).\n"
       "Format requirements:\n"
       "- 1-2 sentence hook\n"
       "- 3-6 short lines/paragraphs with clear spacing\n"
       "- Include 1 practical takeaway or framework\n"
       "- End with a thoughtful question\n"
       "- Avoid excessive emojis (0-1 max)\n"
       "- Use 0-3 hashtags, placed at the end\n"
     ),
     "Youtube": (       
       "You are a YouTube creator.\n"
       "Create YouTube content assets for the topic: {topic}\n\n"
       "Return EXACTLY in this format:\n"
       "TITLE: <max 70 characters>\n"
       "DESCRIPTION:\n"
       "<2 short paragraphs>\n"
       "<3 bullet key points>\n"
       "CHAPTERS:\n"
       "00:00 Intro\n"
       "00:30 <chapter>\n"
       "02:00 <chapter>\n"
       "04:00 <chapter>\n"
       "CTA: <1 sentence>\n"
       "TAGS: <comma-separated tags, 10-15 items>\n\n"
       "Tone: clear, helpful, high-retention, not clickbait.\n"
     )
   }
  # Returns the "Instruction Form" for the platform the user choose
   return PromptTemplate(input_variables=["topic"], template = templates[platform])

def generate_post(*, topic: str, platform: str, api_key: str) -> str:
    """
    Simple LangChain chain: PromptTemplate -> ChatGoogleGenerativeAI -> output string
    """
    # 1. Setup the AI "Brain" (Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,  # Uses your secret key to talk to Google
        # Temperature 0.7 = The "Human" Setting.
        # High (1.0) = Very Creative/Crazy. (Fun but risky)
        # Low (0.1) = Like a Robot/Boring.
        # 0.7 is the "Sweet Spot" for natural writing.
        temperature=0.7,        
    )

    # 2. Get the "Instruction Form" for the chosen platform
    prompt = _platform_prompt(platform)
    
     # 3. # Create the chain using the pipe operator
    chain = prompt | llm

   # 4. Get the answer
    # In 2026, we use .invoke() instead of .run()
    response = chain.invoke({"topic": topic})
    
    # Return the text content
    return response.content.strip()

# This function take the topic,a platform where the content will be posted and API key to access the LLM
def parse_args(argv: list[str]) -> argparse.Namespace:
    # 1. Create the main "Parser" (The tool that reads your commands)
    p = argparse.ArgumentParser(description="Generate platform-specific social content using Gemini.") # # The description shows up if the user types --help in the terminal
    
    p.add_argument("--topic", required=True, help="Topic for the post (e.g., 'AI in healthcare').")
    
    p.add_argument(
        "--platform",
        required=True,
        choices=PLATFORMS,  # Only allows Meta, Instagram, LinkedIn, or YouTube
        help="Target platform: Meta, Instagram, LinkedIn, YouTube.",
    )
    
    p.add_argument(
        "--api-key",
        default="",
        help="Google API key. If omitted, reads from environment variable GOOGLE_API_KEY.",
    )
    
    # Return a "Labeled Box" (Namespace) containing the Topic, Platform, and API Key
    # Namespace(topic='Coffee', platform='Instagram', api_key='') --> # This is what the returned 'args' looks like internally:
    return p.parse_args(argv)
   

def main(argv: list[str]) -> int:
    # STEP 1: Look for the secret API key in a hidden file (.env)
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

    # STEP 2: Get the Topic and Platform from the user's typing
    args = parse_args(argv)

    # STEP 3: Double-check if we have an API key. If not, STOP and show error.
    api_key = (args.api_key or "").strip() or (os.getenv("GOOGLE_API_KEY") or "").strip()
    if not api_key:
        sys.stderr.write("ERROR: Missing Google API key.\n")
        return 2

    # STEP 4: "Action" step
    try:
        result = generate_post(topic=args.topic.strip(), platform=args.platform, api_key=api_key)
        print(result) # Show the final human-like post!
    except Exception as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1
