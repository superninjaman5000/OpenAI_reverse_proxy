from mitmproxy import http
import json
import requests
import os
import guardian_filter

# Require OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("🚨 Missing OpenAI API Key! Set it using 'export OPENAI_API_KEY=your_key_here'")


GUARDIAN_API_URL = "http://localhost:5000/v1/completions"

class OpenAIProxy:
    def request(self, flow: http.HTTPFlow):

        if "api.openai.com" in flow.request.url:
            try:
                # Extract JSON Safely
                data = json.loads(flow.request.get_text())
                messages = data.get("messages", [])
                prompt = messages[-1].get("content", "") if messages else ""

                #  Check if the prompt is allowed
                allowed, reason = guardian_filter.is_prompt_allowed(prompt)

                if not allowed:
                    blocked_message = f'The prompt was blocked due to {reason} content.'
                    flow.response = http.Response.make(
                        403, json.dumps({"error": blocked_message}), {"Content-Type": "application/json"}
                    )
                    return

                #  Inject OpenAI API Key
                flow.request.headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

            except Exception as e:
                error_message = f"Internal Proxy Error: {str(e)}"
                flow.response = http.Response.make(
                    500, json.dumps({"error": error_message}), {"Content-Type": "application/json"}
                )
                print(error_message)

    def response(self, flow: http.HTTPFlow):
        """Intercept OpenAI API responses before returning to the client."""
        if "api.openai.com" in flow.request.url:
            try:
                # Extract OpenAI response safely
                data = json.loads(flow.response.get_text())

                if "choices" in data and data["choices"]:
                    generated_text = data["choices"][0].get("message", {}).get("content", "")

                    #  Only filter if response could be harmful
                    if generated_text and len(generated_text) > 5:
                        allowed, reason = guardian_filter.is_prompt_allowed(generated_text)

                        if not allowed:
                            data["choices"][0]["message"]["content"] = "[Filtered Response]"

                #  Update the response
                flow.response.set_text(json.dumps(data))

            except Exception as e:
                error_message = f"Internal Proxy Error: {str(e)}"
                flow.response.set_text(json.dumps({"error": error_message}))
                print(error_message)

#  Register mitmproxy add-on
addons = [OpenAIProxy()]
