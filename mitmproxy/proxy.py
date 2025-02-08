from mitmproxy import http
import json
import requests
import os
import guardian_filter  # Import the filtering module

# Set IBM Granite Guardian API Endpoint
GUARDIAN_API_URL = os.getenv("GUARDIAN_API_URL", "http://localhost:5000/v1/completions")

# Define block categories
BLOCK_REASONS = ["violent", "illegal", "sexual", "toxic"]

class OpenAIProxy:
    def request(self, flow: http.HTTPFlow):
        """Intercepts OpenAI API requests and applies filtering."""
        if "api.openai.com" in flow.request.url:
            try:
                data = json.loads(flow.request.get_text())

                # Extract user prompt
                prompt = data.get("messages", [{}])[-1].get("content", "")

                # Check if prompt is allowed
                allowed, reason = guardian_filter.is_prompt_allowed(prompt)

                if not allowed:
                    blocked_message = f'The prompt was blocked because it contained {reason} content.'

                    # Block request by sending an HTTP 403 Forbidden response
                    flow.response = http.Response.make(
                        403,  # Forbidden
                        json.dumps({"error": blocked_message}),
                        {"Content-Type": "application/json"},
                    )
                    return  # Stop further request processing
            except Exception as e:
                print(f"[ERROR] Failed to process request: {e}")

    def response(self, flow: http.HTTPFlow):
        """Intercepts and modifies OpenAI API responses before returning to the client."""
        if "api.openai.com" in flow.request.url:
            try:
                data = json.loads(flow.response.get_text())

                # Modify response message only if necessary
                if "choices" in data and len(data["choices"]) > 0:
                    modified_response = "⚠️ [Filtered Response] ⚠️"  # Placeholder modification
                    data["choices"][0]["text"] = modified_response  # Use `.get()` to avoid KeyError

                flow.response.set_text(json.dumps(data))

            except Exception as e:
                print(f"[ERROR] Failed to process response: {e}")

addons = [OpenAIProxy()]
