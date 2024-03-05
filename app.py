import gradio as gr
import torch
import platform
import random
import json
from pathlib import Path
from TTS.api import TTS
import uuid
import html
import soundfile as sf

params = {
    "activate": True,
    "autoplay": True,
    "show_text": False,
    "remove_trailing_dots": False,
    "voice": "Rogger.wav",
    "language": "English",
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
}

# SUPPORTED_FORMATS = ['wav', 'mp3', 'flac', 'ogg']
SAMPLE_RATE = 16000
device = None

# Set the default speaker name
default_speaker_name = "Rogger"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# Load model
def load_model():
    global tts
    print("[XTTS] Loading XTTS...")
    tts = TTS(model_name=params["model_name"]).to(device)
    # model_path=params["model_path"],
    # config_path=params["config_path"]).
    return tts

tts=load_model()

# Voice generation function
def gen_voice(string, spk, speed, english):
    string = html.unescape(string)
    short_uuid = str(uuid.uuid4())[:8]
    fl_name='outputs/' + spk + "-" + short_uuid +'.wav'
    output_file = Path(fl_name)
    this_dir = str(Path(__file__).parent.resolve())
    tts.tts_to_file(
        text=string,
        speed=speed,
        file_path=output_file,
        speaker_wav=[f"{this_dir}/targets/" +spk + ".wav"],
        language=languages[english]
    )
    return output_file

def update_speakers():
    speakers = {p.stem: str(p) for p in list(Path('targets').glob("*.wav"))}
    return list(speakers.keys())

def update_dropdown(_=None, selected_speaker=default_speaker_name):
    return gr.Dropdown(choices=update_speakers(), value=selected_speaker, label="Select Speaker")

# Load the language data
with open(Path('languages.json'), encoding='utf8') as f:
    languages = json.load(f)

# Gradio Blocks interface
with gr.Blocks() as app:
    
    gr.Markdown("### TTS based Voice Cloning.")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines=2, label="Speechify this Text",value="Даже в самые темные ночи одна-единственная искра надежды может зажечь в нас огонь решимости и направить нас к будущему, о котором мы смеем мечтать.")
            speed_slider = gr.Slider(label='Speed', minimum=0.1, maximum=1.99, value=0.8, step=0.01)
            language_dropdown = gr.Dropdown(list(languages.keys()), label="Language/Accent", value="Russian")

            gr.Markdown("### Speaker Selection and Voice Cloning")
            
            with gr.Row():
                with gr.Column():
                    speaker_dropdown = update_dropdown()
                    refresh_button = gr.Button("Refresh Speakers")
                
            refresh_button.click(fn=update_dropdown, inputs=[], outputs=speaker_dropdown)
            submit_button = gr.Button("Convert")

        with gr.Column():
            audio_output = gr.Audio(label="Result")

    submit_button.click(
        fn=gen_voice,
        inputs=[text_input, speaker_dropdown, speed_slider, language_dropdown],
        outputs=audio_output
    )

if __name__ == "__main__":
    app.launch()