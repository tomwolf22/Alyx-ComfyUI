import requests
import os

class PollinationsEdit:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {}),
                "image_url": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "api"

    def run(self, prompt, image_url):
        key = os.environ.get("POLLINATIONS_API_KEY")

        url = (
            "https://gen.pollinations.ai/image/"
            f"{prompt}"
            f"?model=qwen-image"
            f"&width=1024"
            f"&height=1024"
            f"&seed=0"
            f"&enhance=true"
            f"&image={image_url}"
            f"&key={key}"
        )

        r = requests.get(url)
        return (r.text,)


NODE_CLASS_MAPPINGS = {
    "PollinationsEdit": PollinationsEdit
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pollinations Edit": "Pollinations Edit Engine"
}
