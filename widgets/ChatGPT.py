import os
import openai
#load the .env file
from dotenv import load_dotenv
load_dotenv()
openai.organization = "org-XsjX7pgRFpwuIEAZvkKojg0p"
openai.api_key = os.getenv("OPENAI_API_KEY")

def response(messages):
	assert isinstance(messages, list)
	for msg in messages:
		assert "role" in msg
		assert "content" in msg

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
			messages=messages
		)

	return completion.choices[0].message['content']


if __name__ == "__main__":
	messages = [
		{"role": "user", "content": "please respond."}
	]
	print(response(messages))