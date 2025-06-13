#!/usr/bin/env python3
"""
API Key Setup Script for SkillMate AI
"""

import os
import json
import sys

def setup_api_keys():
    """Set up API keys for SkillMate AI."""
    print("SkillMate AI - API Key Setup")
    print("============================")
    
    # Create directory if it doesn't exist
    ai_dir = os.path.join("skillmate", "ai")
    os.makedirs(ai_dir, exist_ok=True)
    
    api_keys_file = os.path.join(ai_dir, "api_keys.txt")
    
    # Check if file already exists
    if os.path.exists(api_keys_file):
        overwrite = input(f"API keys file already exists at {api_keys_file}. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Get API keys from user
    print("\nEnter your API keys (press Enter to skip):")
    openai_keys = []
    gemini_keys = []
    
    # OpenAI keys
    print("\nOpenAI API Keys (format: sk-...)")
    while True:
        key = input(f"OpenAI API Key #{len(openai_keys) + 1} (or Enter to finish): ")
        if not key:
            break
        if not key.startswith("sk-"):
            print("Invalid key format. OpenAI keys should start with 'sk-'")
            continue
        openai_keys.append(key)
    
    # Gemini keys
    print("\nGemini API Keys")
    while True:
        key = input(f"Gemini API Key #{len(gemini_keys) + 1} (or Enter to finish): ")
        if not key:
            break
        gemini_keys.append(key)
    
    # Write keys to file
    with open(api_keys_file, "w") as f:
        for key in openai_keys:
            f.write(f"{key}\n")
        for key in gemini_keys:
            f.write(f"{key}\n")
    
    print(f"\nAPI keys saved to {api_keys_file}")
    print(f"Total keys: {len(openai_keys)} OpenAI keys, {len(gemini_keys)} Gemini keys")
    print("\nYou can also set API keys as environment variables:")
    print("  export OPENAI_API_KEY=your-api-key")
    print("  export GEMINI_API_KEY=your-api-key")

if __name__ == "__main__":
    setup_api_keys() 