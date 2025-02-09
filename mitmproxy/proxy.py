from mitmproxy import http
import json
import guardian_filter  # Import the filtering module

class OpenAIProxy:
    def request(self, flow: http.HTTPFlow):
        """Intercepts OpenAI API requests and applies filtering."""
        if "api.openai.com" in flow.request.url:
            try:
                data = json.loads(flow.request.get_text())

                # Extract user prompt
                prompt = data.get("messages", [{}])[-1].get("content", "")

                # Check if the prompt is allowed
                allowed, reason = guardian_filter.is_prompt_allowed(prompt)

                if not allowed:
                    blocked_message = f'The prompt was blocked due to {reason} content.'
                    flow.response = http.Response.make(
                        403,  # HTTP Forbidden
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
                    modified_response = data["choices"][0]["message"]["content"]

                    # Log filtered response for debugging
                    print(f"[INFO] Response from OpenAI: {modified_response}")

                flow.response.set_text(json.dumps(data))

            except Exception as e:
                print(f"[ERROR] Failed to process response: {e}")

addons = [OpenAIProxy()]
