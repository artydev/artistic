import streamlit as st
from gradio_client import Client
import base64
import io
from PIL import Image

# Initialize the Gradio client
client = Client("https://pixart-alpha-pixart-lcm.hf.space/--replicas/mz7f1/")

def predict(prompt, negative_prompt, image_style, use_negative_prompt, seed, width, height, lcm_inference_steps, randomize_seed):
    result = client.predict(
        prompt,
        negative_prompt,
        image_style,
        use_negative_prompt,
        seed,
        width,
        height,
        lcm_inference_steps,
        randomize_seed,
        api_name="/run"
    )
    # Assuming the result is a dictionary with an 'image' key containing base64 encoded image data
    return result

def display_image(image_base64):
    # Convert base64 to bytes
    image_bytes = base64.b64decode(image_base64)
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    # Display the image
    st.image(image, caption='Generated Image', use_column_width=True)

# Streamlit app layout
st.title('From Imagination to Image...')

if 'form' not in st.session_state:
    st.session_state.form = {
        'prompt': '',
        'negative_prompt': '',
        'image_style': '(No style)',
        'use_negative_prompt': False,
        'seed': 45646546,
        'width': 1024,
        'height': 1024,
        'lcm_inference_steps': 15,
        'randomize_seed': False
    }

# Form inputs
with st.form(key='my_form'):
    st.session_state.form['prompt'] = st.text_input("Prompt", value=st.session_state.form.get('prompt', ''))
    st.session_state.form['negative_prompt'] = st.text_input("Negative Prompt", value=st.session_state.form.get('negative_prompt', ''))
    st.session_state.form['image_style'] = st.selectbox("Image Style", ["(No style)", "Cinematic", "Photographic", "Anime", "Manga", "Digital Art", "Pixel art", "Fantasy art", "Neonpunk", "3D Model"], index=st.session_state.form['image_style'].index(st.session_state.form['image_style']))
    st.session_state.form['use_negative_prompt'] = st.checkbox("Use Negative Prompt", value=st.session_state.form.get('use_negative_prompt', False))
    st.session_state.form['seed'] = st.slider("Seed", min_value=0, max_value=2147483647, value=st.session_state.form.get('seed', 6576577))
    st.session_state.form['width'] = st.slider("Width", min_value=256, max_value=2048, value=st.session_state.form.get('width', 1024))
    st.session_state.form['height'] = st.slider("Height", min_value=256, max_value=2048, value=st.session_state.form.get('height', 1024))
    st.session_state.form['lcm_inference_steps'] = st.slider("LCM Inference Steps", min_value=1, max_value=30, value=st.session_state.form.get('lcm_inference_steps', 15))
    st.session_state.form['randomize_seed'] = st.checkbox("Randomize Seed", value=st.session_state.form.get('randomize_seed', False))

    # Submit button
    submitted = st.form_submit_button(label='Generate')

# Process form submission
if submitted:
    result = predict(st.session_state.form['prompt'], st.session_state.form['negative_prompt'], st.session_state.form['image_style'], st.session_state.form['use_negative_prompt'], st.session_state.form['seed'], st.session_state.form['width'], st.session_state.form['height'], st.session_state.form['lcm_inference_steps'], st.session_state.form['randomize_seed'])
    image_path = result[0][0]['image']
    
    with open(image_path, "rb") as image_file:
        # Read the contents of the file
        image_data = image_file.read()
        # Encode the contents to base64
        base64_encoded_image = base64.b64encode(image_data)
        display_image(base64_encoded_image)
