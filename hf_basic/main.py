from transformers import pipeline

pipe = pipeline("image-to-text-generation", model="google/gemma-3-4b-it")

message = [
    {
        "role": "user", 
        "content": [
            {"type":"image", "url":"https://huggingface.co/datasets/hf-internal-testing/diffusers-images/resolve/main/00000.png"},
            {"type":"text", "text":"Describe the image in detail."}
        ]
    },
]