import urllib.request
import urllib.parse
import json
import os
import time

# Load token from environment or ask for it
hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    # Try reading from a local .env file if it exists
    if os.path.exists(".env"):
        with open(".env", "r") as env_file:
            for line in env_file:
                if line.startswith("HF_TOKEN="):
                    hf_token = line.split("=", 1)[1].strip()
                    break

if not hf_token:
    print("HF_TOKEN not found in environment variables or .env file.")
    hf_token = input("Please enter your Hugging Face API token: ").strip()

if not hf_token:
    print("Error: Hugging Face API token is required.")
    exit(1)

model_id = "black-forest-labs/FLUX.1-schnell"
url = f"https://router.huggingface.co/hf-inference/models/{model_id}"

prompt = "A premium, realistic, mouth-watering close-up photography of Aloo Gobi Masala, potato cubes and cauliflower florets sautéed with ginger and Indian spices, served in a dark ceramic dish, garnished with coriander. Dark background, cinematic lighting, food photography."

print(f"Generating image using {model_id}...")
data = json.dumps({"inputs": prompt}).encode("utf-8")

req = urllib.request.Request(
    url,
    data=data,
    headers={
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    },
    method="POST"
)

start_time = time.time()
try:
    with urllib.request.urlopen(req) as response:
        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type:
            # Hugging Face API might return JSON if the model is loading
            res_data = json.loads(response.read().decode("utf-8"))
            if "error" in res_data:
                print("API Error:", res_data["error"])
                if "loading" in res_data.get("error", "").lower():
                    # The model is loading, wait and retry
                    estimated_time = res_data.get("estimated_time", 20)
                    print(f"Model is loading. Estimated time: {estimated_time}s. Please wait...")
                    time.sleep(estimated_time)
                    # Retry once
                    with urllib.request.urlopen(req) as retry_response:
                        with open("test_hf_aloo_gobi.png", "wb") as f:
                            f.write(retry_response.read())
                else:
                    exit(1)
            else:
                print("Unexpected JSON response:", res_data)
                exit(1)
        else:
            # Binary image response
            with open("test_hf_aloo_gobi.png", "wb") as f:
                f.write(response.read())
            
    duration = time.time() - start_time
    print(f"Success! Saved as test_hf_aloo_gobi.png in {duration:.2f} seconds. File size: {os.path.getsize('test_hf_aloo_gobi.png')} bytes.")
except Exception as e:
    print("Error during request:", e)
