import sys
import json
import requests
import time
import threading
from bs4 import BeautifulSoup
from random import randint as rr

def generate_user_agent():
    return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/{rr(50, 120)}.0.{rr(2000, 5000)}.{rr(60, 170)} Safari/537.36"

def get_video_url(url):
    headers = {
        'Accept': 'application/json',
        'User-Agent': generate_user_agent(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'id': requests.utils.unquote(url), 'locale': 'en'}
    try:
        response = requests.post('https://getmyfb.com/process', data=data, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.select('li.results-list-item'):
            quality_text = item.get_text(strip=True)
            link = item.find('a')['href'] if item.find('a') else None
            if quality_text and link:
                quality = quality_text.split('(')[0].strip()
                if '720p' in quality:
                    return link
                elif '360p' in quality:
                    return link
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting video URL: {e}")
        return None

def loading_animation():
    loading_chars = ['|', '/', '-', '\\']
    while True:
        for char in loading_chars:
            print(f"\rLoading... {char}", end="")
            time.sleep(0.2)

def download_video(url, filename):
    try:
        headers = {
            'User-Agent': generate_user_agent(),
            'Accept': 'application/json',
            'Referer': url
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"\nVideo downloaded successfully as {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else input("Enter Facebook video URL: ")
    video_url = get_video_url(url)
    if video_url:
        print("Starting download 720p (HD)")
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.daemon = True
        loading_thread.start()
        download_video(video_url, filename="AntonThomzz_720p.mp4")
    else:
        print("No video URL found for download.")

if __name__ == '__main__':
    main()