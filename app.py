#!/usr/bin/env python3
"""
Christian Portrait Generator with FLUX
Professional Streamlit App for Custom Portrait Generation
"""

import streamlit as st
import requests
import time
import os
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Christian Portrait Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()

# Configuration
FINETUNE_ID = "17547232-bbdf-409b-91c9-a8a510286857"
# Récupérer la clé API depuis .streamlit/secrets.toml
BFL_API_KEY = st.secrets["BFL_API_KEY"]
API_BASE_URL = "https://api.us1.bfl.ai/v1"
TRIGGER_WORD = "christian_1234_tok"

def generate_image(prompt, finetune_strength=1.2, aspect_ratio="1:1", steps=30, raw_mode=True):
    """Generate image with Christian fine-tuned model using aspect_ratio"""
    
    headers = {
        "Content-Type": "application/json",
        "X-Key": BFL_API_KEY
    }
    
    payload = {
        "prompt": prompt,
        "finetune_id": FINETUNE_ID,
        "finetune_strength": finetune_strength,
        "aspect_ratio": aspect_ratio,  # Use aspect_ratio parameter instead of width/height
        "steps": steps,
        "raw": raw_mode
    }
    
    # Launch generation
    response = requests.post(
        f"{API_BASE_URL}/flux-pro-1.1-ultra-finetuned",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        st.error(f"Generation error: {response.status_code} - {response.text}")
        return None
    
    task_data = response.json()
    task_id = task_data.get("id")
    
    if not task_id:
        st.error("No task_id received")
        return None
    
    # Polling for result
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for attempt in range(60):  # Max 60 attempts (3 minutes)
        time.sleep(3)
        
        # Check status
        result_response = requests.get(
            f"{API_BASE_URL}/get_result?id={task_id}",
            headers=headers
        )
        
        if result_response.status_code == 200:
            result = result_response.json()
            status = result.get("status")
            
            if status == "Ready":
                progress_bar.progress(100)
                status_text.success("Image generated successfully!")
                return result.get("result", {}).get("sample")
            
            elif status == "Failed":
                st.error("Generation failed")
                return None
            
            else:
                # In progress
                progress = min((attempt + 1) * 100 // 20, 95)
                progress_bar.progress(progress)
                status_text.info(f"Generating... ({status})")
        
        else:
            st.error(f"Status check error: {result_response.status_code}")
            return None
    
    st.error("Timeout - Generation taking too long")
    return None

def download_image(image_url):
    """Download image from URL"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Download error: {e}")
        return None

def get_download_link(img, filename):
    """Create download link for image"""
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/jpeg;base64,{img_str}" download="{filename}" style="text-decoration: none; background-color: #0066cc; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block;">Download Image</a>'
    return href

# Main interface
def main():
    # Header
    st.title("Christian Portrait Generator")
    st.markdown("*Create custom portraits using AI-powered FLUX technology*")
    st.divider()
    
    # API key check
    if not BFL_API_KEY:
        st.error("BFL API key missing! Add your API key in .env file: BFL_API_KEY=your_key")
        return
    
    # Main layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Prompt Configuration")
        
        # Creative prompt templates
        prompt_categories = {
            "Professional Portraits": [
                f"{TRIGGER_WORD}, executive headshot, tailored black suit, white shirt, confident expression, modern office background",
                f"{TRIGGER_WORD}, corporate portrait, navy blue blazer, professional lighting, neutral background",
                f"{TRIGGER_WORD}, business casual, smart shirt, friendly smile, contemporary office setting",
                f"{TRIGGER_WORD}, LinkedIn style portrait, formal attire, professional backdrop, direct gaze"
            ],
            
            "Creative & Artistic": [
                f"{TRIGGER_WORD}, riding a magnificent white horse, medieval knight armor, dramatic landscape background",
                f"{TRIGGER_WORD}, sitting on a vintage motorcycle, leather jacket, sunset highway backdrop",
                f"{TRIGGER_WORD}, as a Renaissance nobleman, ornate period costume, classical painting style",
                f"{TRIGGER_WORD}, steampunk gentleman, brass goggles, mechanical background, Victorian era clothing",
                f"{TRIGGER_WORD}, space commander uniform, futuristic setting, sci-fi lighting effects",
                f"{TRIGGER_WORD}, as a detective in film noir style, trench coat, shadowy urban alley"
            ],
            
            "Lifestyle & Casual": [
                f"{TRIGGER_WORD}, casual weekend portrait, denim jacket, natural outdoor lighting, relaxed smile",
                f"{TRIGGER_WORD}, beach vacation style, summer shirt, ocean background, golden hour lighting",
                f"{TRIGGER_WORD}, urban street style, trendy outfit, city backdrop, contemporary fashion",
                f"{TRIGGER_WORD}, cozy cafe setting, casual sweater, warm interior lighting, coffee shop ambiance"
            ],
            
            "Historical & Fantasy": [
                f"{TRIGGER_WORD}, as a Roman centurion, authentic armor, ancient battlefield setting",
                f"{TRIGGER_WORD}, Victorian gentleman, top hat and formal coat, 19th century London street",
                f"{TRIGGER_WORD}, pirate captain, tricorn hat, aboard sailing ship, oceanic adventure",
                f"{TRIGGER_WORD}, Wild West sheriff, cowboy hat and badge, dusty frontier town",
                f"{TRIGGER_WORD}, medieval scholar, robes and scrolls, ancient library setting"
            ],
            
            "Action & Adventure": [
                f"{TRIGGER_WORD}, mountain climber, expedition gear, dramatic alpine landscape",
                f"{TRIGGER_WORD}, rally car driver, racing suit and helmet, motorsport environment",
                f"{TRIGGER_WORD}, deep sea explorer, diving equipment, underwater adventure scene",
                f"{TRIGGER_WORD}, aircraft pilot, aviator uniform, vintage airplane cockpit"
            ]
        }
        
        # Category selection
        selected_category = st.selectbox("Choose a category:", ["Custom Prompt"] + list(prompt_categories.keys()))
        
        if selected_category != "Custom Prompt":
            selected_prompt = st.selectbox("Select a scenario:", prompt_categories[selected_category])
            if st.button("Use this prompt"):
                st.session_state.selected_prompt = selected_prompt
        
        # Custom prompt area
        if selected_category == "Custom Prompt":
            default_prompt = f"{TRIGGER_WORD}, "
        else:
            default_prompt = st.session_state.get('selected_prompt', f"{TRIGGER_WORD}, ")
        
        prompt = st.text_area(
            "Enter your prompt:",
            value=default_prompt,
            height=120,
            help=f"Always start with '{TRIGGER_WORD}' for best results"
        )
        
        # Prompt validation
        if not prompt.lower().startswith(TRIGGER_WORD.lower()):
            st.warning(f"Your prompt should start with '{TRIGGER_WORD}' for optimal results")
        
        # Advanced settings in expander
        with st.expander("Advanced Settings"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                finetune_strength = st.slider("Character Strength", 0.5, 2.0, 1.2, 0.1)
                
                # Format selection with BFL API compatible aspect ratios
                format_options = {
                    "Portrait (3:4)": "3:4",
                    "Square (1:1)": "1:1", 
                    "Landscape (4:3)": "4:3",
                    "Wide (16:9)": "16:9",
                    "Ultra Wide (21:9)": "21:9",
                    "Instagram Story (9:16)": "9:16",
                    "Cinema (2.35:1)": "2.35:1",
                    "Standard (4:5)": "4:5"
                }
                
                selected_format = st.selectbox("Photo Format", list(format_options.keys()), index=1)
                aspect_ratio = format_options[selected_format]
                
                # Display selected ratio
                st.caption(f"Aspect Ratio: {aspect_ratio}")
            
            with col_b:
                quality_options = {
                    "Fast (20 steps)": 20,
                    "Balanced (30 steps)": 30,
                    "High Quality (40 steps)": 40,
                    "Ultra (50 steps)": 50
                }
                
                selected_quality = st.selectbox("Quality", list(quality_options.keys()), index=1)
                steps = quality_options[selected_quality]
                
                raw_mode = st.checkbox("Photorealistic Mode", value=True)
        
        # Generate button
        generate_btn = st.button("Generate Portrait", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Generated Image")
        
        # Image display area with better spacing
        image_container = st.container()
        
        if generate_btn and prompt.strip():
            with image_container:
                # Generate image
                image_url = generate_image(
                    prompt=prompt,
                    finetune_strength=finetune_strength,
                    aspect_ratio=aspect_ratio,
                    steps=steps,
                    raw_mode=raw_mode
                )
                
                if image_url:
                    # Download and display image
                    img = download_image(image_url)
                    
                    if img:
                        # Display image with optimal sizing
                        st.image(img, use_container_width=True, caption=f"Generated at {datetime.now().strftime('%H:%M:%S')}")
                        
                        # Compact info display
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.caption(f"Format: {selected_format}")
                        with col_info2:
                            st.caption(f"Quality: {selected_quality}")
                        
                        # Download button
                        filename = f"christian_portrait_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        download_link = get_download_link(img, filename)
                        st.markdown(download_link, unsafe_allow_html=True)
                        
                        st.success("Image generated successfully!")
                        
                        # Compact regenerate button
                        if st.button("Generate New Variation", use_container_width=True):
                            st.rerun()
                        
                        # Show generation parameters in collapsible section
                        with st.expander("Generation Details"):
                            st.write(f"**Prompt:** {prompt}")
                            st.write(f"**Character Strength:** {finetune_strength}")
                            st.write(f"**Aspect Ratio:** {aspect_ratio}")
                            st.write(f"**Steps:** {steps}")
                            st.write(f"**Photorealistic:** {'Yes' if raw_mode else 'No'}")
        
        elif generate_btn and not prompt.strip():
            st.error("Please enter a prompt")
        
        else:
            # Show format preview when no image
            st.info("Select a prompt and click 'Generate Portrait' to create your image")
            if 'selected_format' in locals():
                # Create a visual preview of the aspect ratio
                ratio_parts = aspect_ratio.split(':')
                ratio_w, ratio_h = float(ratio_parts[0]), float(ratio_parts[1])
                ratio_value = ratio_w / ratio_h
                
                if ratio_value > 1:
                    preview_width = 300
                    preview_height = int(300 / ratio_value)
                else:
                    preview_height = 300
                    preview_width = int(300 * ratio_value)
                
                # Create a placeholder showing the format
                placeholder_html = f"""
                <div style="
                    width: {preview_width}px; 
                    height: {preview_height}px; 
                    border: 2px dashed #ccc; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    margin: 20px auto;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                ">
                    <div style="text-align: center; color: #666;">
                        <div style="font-weight: bold;">{selected_format}</div>
                        <div style="font-size: 12px;">{aspect_ratio}</div>
                    </div>
                </div>
                """
                st.markdown(placeholder_html, unsafe_allow_html=True)
    
    # Model information footer
    st.divider()
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Model", "FLUX Pro 1.1 Ultra")
    
    with col_info2:
        st.metric("Trigger Word", TRIGGER_WORD)
    
    with col_info3:
        st.metric("Aspect Ratio", "Dynamic")

if __name__ == "__main__":
    main()
