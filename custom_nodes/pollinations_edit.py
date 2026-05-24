import os
import requests
import urllib.parse
import numpy as np
import torch
from PIL import Image
import io

class PollinationsEdit:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url": ("STRING", {}),
                "prompt": ("STRING", {"multiline": True}),
                "unet_name": ("STRING", {"default": "qwen-image"}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "pollinations"

    def run(self, image_url, prompt, unet_name, width, height):
        key = os.environ.get("POLLINATIONS_API_KEY")

        # encode prompt safely
        safe_prompt = urllib.parse.quote(prompt, safe="")

        # prevent double-encoding image URLs
        if "%3A" in image_url or "%2F" in image_url:
            safe_image = image_url
        else:
            safe_image = urllib.parse.quote(image_url, safe="")

        url = (
            "https://gen.pollinations.ai/image/"
            f"{safe_prompt}"
            f"?model=qwen-image"
            f"&width={width}"
            f"&height={height}"
            f"&enhance=true"
            f"&image={safe_image}"
            f"&key={key}"
        )

        r = requests.get(url)
        r.raise_for_status()

        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]

        return (img,)


NODE_CLASS_MAPPINGS = {
    "PollinationsEdit": PollinationsEdit
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pollinations Edit": "Pollinations Edit"
}
