import requests
import os

# Define IBM Granite Guardian API URL
GUARDIAN_API_URL = "http://localhost:5000/v1/completions"

# Define block categories
BLOCK_CATEGORIES = ["violent", "illegal", "sexual", "toxic"]

def classify_text(text):
    """Sends text to IBM Granite Guardian and returns classification."""
    payload = {
        "model": "ibm/granite-guardian",
        "prompt": f"Classify this text: {text}",
        "max_tokens": 10
    }

    try:
        response = requests.post(GUARDIAN_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract classification label 
        classification = result.get("choices", [{}])[0].get("text", "safe").strip().lower()

        if classification in BLOCK_CATEGORIES:
            return classification  # Block the request
        return "safe"
    except Exception as e:
        print(f"Error contacting Guardian API: {e}")
        return "error"

def is_prompt_allowed(prompt):
    """Checks if the prompt is safe or should be blocked."""
    classification = classify_text(prompt)
    
    if classification in BLOCK_CATEGORIES:
        return False, classification
    return True, "safe"

if __name__ == "__main__":
    test_prompt = input("Enter a test prompt: ")
    allowed, reason = is_prompt_allowed(test_prompt)
    
    if allowed:
        print(" Prompt is safe!")
    else:
        print(f"Blocked: {reason}")
