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
                "prompt": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "pollinations"

    def run(self, image_url, prompt):
        key = os.environ.get("POLLINATIONS_API_KEY")

        # encode prompt once (always safe)
        safe_prompt = urllib.parse.quote(prompt, safe="")

        # SAFE: prevent double encoding
        # only encode if it is NOT already encoded
        if "%3A" in image_url or "%2F" in image_url:
            safe_image = image_url
        else:
            safe_image = urllib.parse.quote(image_url, safe="")

        url = (
            "https://gen.pollinations.ai/image/"
            f"{safe_prompt}"
            f"?model=qwen-image"
            f"&width=1024"
            f"&height=1024"
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
