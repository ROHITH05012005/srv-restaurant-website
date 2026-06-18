import urllib.request
import urllib.parse
import time

def test_proxy():
    # Let's fetch the list of proxies
    print("Fetching proxy list...")
    proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
    req_proxy = urllib.request.Request(proxy_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        proxies_data = urllib.request.urlopen(req_proxy).read().decode('utf-8')
        proxies = [p.strip() for p in proxies_data.split('\n') if p.strip()]
        print(f"Loaded {len(proxies)} proxies.")
    except Exception as e:
        print(f"Failed to fetch proxies: {e}")
        return

    # Try downloading with a few proxies until one works
    prompt = "A premium close-up of a cup of tea"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&private=true&enhance=false"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    success = False
    for i, p in enumerate(proxies[:15]):
        print(f"[{i+1}/15] Trying proxy: {p} ... ", end="", flush=True)
        proxy_handler = urllib.request.ProxyHandler({'http': p, 'https': p})
        opener = urllib.request.build_opener(proxy_handler)
        
        start = time.time()
        try:
            # We set a short timeout so we don't hang too long on bad proxies
            with opener.open(req, timeout=12) as response:
                content = response.read()
            elapsed = time.time() - start
            if len(content) > 1000:
                print(f"SUCCESS! Loaded {len(content)} bytes in {elapsed:.1f}s")
                success = True
                with open("test_tea_proxy.png", "wb") as f:
                    f.write(content)
                break
            else:
                print(f"Returned small content: {len(content)} bytes")
        except Exception as e:
            elapsed = time.time() - start
            print(f"Failed ({e}) in {elapsed:.1f}s")

    if not success:
        print("Could not download image using any of the tested proxies.")

if __name__ == "__main__":
    test_proxy()
