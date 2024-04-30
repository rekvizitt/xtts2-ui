from gradio_client import Client
import sys

args = sys.argv

# model_name = args[1]
user_input = args[1]

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		f"{user_input}",
		"girl",
		1.99,
		"Russian",
        api_name="/gen_voice"
)
print(result)