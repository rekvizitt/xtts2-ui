from gradio_client import Client
import sys

args = sys.argv

# model_name = args[1]
user_input = args[1]

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		f"{user_input}",	# str  in 'Speechify this Text' Textbox component
		"Rogger",	# Literal[Rogger]  in 'Select Speaker' Dropdown component
		0.8,	# float (numeric value between 0.1 and 1.99) in 'Speed' Slider component
		"Russian",	# Literal[Arabic, Chinese, Czech, Dutch, English, French, German, Hungarian, Italian, Japanese, Korean, Polish, Portuguese, Russian, Spanish, Turkish]  in 'Language/Accent' Dropdown component
        api_name="/gen_voice"
)
print(result)