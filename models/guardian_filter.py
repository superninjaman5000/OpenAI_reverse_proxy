import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# IBM Granite Guardian API URL
GUARDIAN_API_URL = "http://localhost:5000/v1/completions"

# Define the classification model
MODEL_NAME = "ibm-granite/granite-guardian-3.1-2b"

def classify_text(text):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Does this text contain illegal, violent, sexual, or toxic content? Reply 'Safe' or a category: \"{text}\"",
        "temperature": 0.0,  # Force deterministic output
        "max_tokens": 10
    }

    try:
        response = requests.post(GUARDIAN_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract classification label safely
        choices = result.get("choices", [])
        if choices and "text" in choices[0]:
            classification = choices[0]["text"].strip().lower()
        else:
            classification = "safe"  # Default to safe if response is invalid

        logging.info(f"Guardian classified text as: {classification}")
        return classification
    except Exception as e:
        logging.error(f"Guardian API Error: {e}")
        return "error"

def is_prompt_allowed(prompt):
    """Checks if the prompt is safe or should be blocked."""
    classification = classify_text(prompt)

    if classification != "safe":
        return False, classification
    return True, "safe"

if __name__ == "__main__":
    test_prompt = input("Enter a test prompt: ")
    allowed, reason = is_prompt_allowed(test_prompt)

    if allowed:
        print(" Prompt is safe!")
    else:
        print(f" Blocked: {reason}")
