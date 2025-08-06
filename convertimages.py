#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from PIL import Image
import io

# Supported image types
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')

# Max file size in bytes (50 KB)
MAX_FILE_SIZE = 50 * 1024

# Target dimensions
TARGET_WIDTH = 1200
TARGET_HEIGHT = 628

# List all images in current folder
image_files = [f for f in os.listdir('.') if f.lower().endswith(IMAGE_EXTENSIONS)]

for image_file in image_files:
    try:
        print(f"Processing: {image_file}")
        img = Image.open(image_file).convert("RGBA")

        # Resize and crop from center
        img_ratio = img.width / img.height
        target_ratio = TARGET_WIDTH / TARGET_HEIGHT

        if img_ratio > target_ratio:
            # Image is wider than target aspect ratio
            new_height = TARGET_HEIGHT
            new_width = int(TARGET_HEIGHT * img_ratio)
        else:
            # Image is taller than target aspect ratio
            new_width = TARGET_WIDTH
            new_height = int(TARGET_WIDTH / img_ratio)

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Center crop
        left = (new_width - TARGET_WIDTH) // 2
        top = (new_height - TARGET_HEIGHT) // 2
        right = left + TARGET_WIDTH
        bottom = top + TARGET_HEIGHT

        img_cropped = img_resized.crop((left, top, right, bottom))

        webp_filename = os.path.splitext(image_file)[0] + ".webp"

        # Try compressing within size limit
        for quality in range(85, 10, -5):
            buffer = io.BytesIO()
            img_cropped.save(buffer, format='WEBP', quality=quality, method=6)
            size = buffer.tell()
            if size <= MAX_FILE_SIZE:
                with open(webp_filename, 'wb') as f:
                    f.write(buffer.getvalue())
                print(f"Saved {webp_filename} at quality {quality} ({size // 1024} KB)")
                break
        else:
            print(f"Failed to compress {image_file} under {MAX_FILE_SIZE // 1024} KB")

    except Exception as e:
        print(f"Error processing {image_file}: {e}")


# In[1]:


import streamlit as st
from PIL import Image
import io

# Settings
MAX_FILE_SIZE = 50 * 1024  # 50 KB
TARGET_WIDTH = 1200
TARGET_HEIGHT = 628

st.title("🖼 Image Resizer & Compressor (WEBP)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        img = Image.open(uploaded_file).convert("RGBA")

        # Resize while keeping aspect ratio
        img_ratio = img.width / img.height
        target_ratio = TARGET_WIDTH / TARGET_HEIGHT

        if img_ratio > target_ratio:
            new_height = TARGET_HEIGHT
            new_width = int(TARGET_HEIGHT * img_ratio)
        else:
            new_width = TARGET_WIDTH
            new_height = int(TARGET_WIDTH / img_ratio)

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Center crop
        left = (new_width - TARGET_WIDTH) // 2
        top = (new_height - TARGET_HEIGHT) // 2
        right = left + TARGET_WIDTH
        bottom = top + TARGET_HEIGHT
        img_cropped = img_resized.crop((left, top, right, bottom))

        # Compress to WEBP under 50 KB
        webp_bytes = None
        for quality in range(85, 10, -5):
            buffer = io.BytesIO()
            img_cropped.save(buffer, format='WEBP', quality=quality, method=6)
            size = buffer.tell()
            if size <= MAX_FILE_SIZE:
                webp_bytes = buffer.getvalue()
                break

        if webp_bytes:
            st.image(img_cropped, caption="Processed Image", use_column_width=True)
            st.download_button(
                label="Download Processed Image (WEBP)",
                data=webp_bytes,
                file_name="processed_image.webp",
                mime="image/webp"
            )
            st.success(f"Image processed and compressed to {len(webp_bytes)//1024} KB")
        else:
            st.error("Failed to compress under 50 KB. Try a smaller image.")

    except Exception as e:
        st.error(f"Error: {e}")


# In[ ]:




