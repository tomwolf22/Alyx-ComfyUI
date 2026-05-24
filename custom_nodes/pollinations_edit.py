import os
import requests

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

        url = (
            "https://gen.pollinations.ai/image/"
            f"{prompt}"
            f"?model=qwen-image"
            f"&width=1024"
            f"&height=1024"
            f"&enhance=true"
            f"&image={image_url}"
            f"&key={key}"
        )

        # return image URL directly (ComfyUI accepts URL in IMAGE pipe)
        return (url,)
        

NODE_CLASS_MAPPINGS = {
    "PollinationsEdit": PollinationsEdit
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pollinations Edit": "Pollinations Edit"
}
