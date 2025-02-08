import openai
import os

# put your api key between the qoutes, this would be better to use an environment variable instead for security IE:
    # api_key=os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(api_key="use your own api key here")

def send_prompt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", #here you can choose the model, gpt-4o-mini
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    prompt = input("Enter your message: ")
    print(send_prompt(prompt))
