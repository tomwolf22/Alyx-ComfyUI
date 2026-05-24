import os
import requests
import numpy as np
import torch
from PIL import Image
import io


class PollinationsEdit:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True}),
                "unet_name": ("STRING", {"default": "qwen-image"}),
                "width": ("INT", {"default": 1024}),
                "height": ("INT", {"default": 1024}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "pollinations"

    def run(self, image, prompt, unet_name, width, height):

        # -----------------------------
        # 1. Convert tensor → image
        # -----------------------------
        if len(image.shape) == 4:
            image = image[0]

        image = (image * 255).clip(0, 255).astype(np.uint8)

        pil_img = Image.fromarray(image)

        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        buf.seek(0)

        # -----------------------------
        # 2. Call Pollinations
        # -----------------------------
        key = os.environ.get("POLLINATIONS_API_KEY")

        url = (
            f"https://gen.pollinations.ai/image/"
            f"{requests.utils.quote(prompt)}"
            f"?model={unet_name}"
            f"&width={width}"
            f"&height={height}"
            f"&enhance=true"
            f"&key={key}"
        )

        r = requests.post(url, files={"image": buf})
        r.raise_for_status()

        # -----------------------------
        # 3. Return result
        # -----------------------------
        out = Image.open(io.BytesIO(r.content)).convert("RGB")
        out = np.array(out).astype(np.float32) / 255.0
        out = torch.from_numpy(out)[None,]

        return (out,)


NODE_CLASS_MAPPINGS = {
    "PollinationsEdit": PollinationsEdit
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pollinations Edit": "Pollinations Edit"
}
