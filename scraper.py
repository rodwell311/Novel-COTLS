import requests
from bs4 import BeautifulSoup
import json
import time
from deep_translator import GoogleTranslator
import os

# Configuration
BASE_URL = "https://levelingods.shop/novel/chronicles-of-the-lazy-sovereign-novel/chapter-1/"
OUTPUT_FILE = "novel_data.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def translate_text(text):
    try:
        # Split text into chunks if too long (simple approach)
        if len(text) > 4500:
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translated_chunks = [GoogleTranslator(source='auto', target='id').translate(chunk) for chunk in chunks]
            return "".join(translated_chunks)
        return GoogleTranslator(source='auto', target='id').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def scrape_novel():
    current_url = BASE_URL
    chapters = []
    chapter_count = 0
    
    # Load existing data if available to resume
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            try:
                chapters = json.load(f)
                if chapters:
                    print(f"Loaded {len(chapters)} existing chapters.")
                    chapter_count = len(chapters)
                    last_chapter = chapters[-1]
                    print(f"Resuming from after Chapter {last_chapter['id']}")
                    
                    # Fetch last chapter page to get the next link
                    soup = get_soup(last_chapter['url'])
                    if soup:
                        next_btn = soup.find('a', string=lambda text: text and 'Next' in text) or \
                                   soup.find('a', class_='next_page')
                        if next_btn and 'href' in next_btn.attrs:
                            current_url = next_btn['href']
                        else:
                            current_url = None
            except Exception as e:
                print(f"Error loading existing data: {e}")
                pass

    print(f"Starting scrape from: {current_url}")

    while current_url:
        # Check limit
        if chapter_count >= 358:
            print("Target of 358 chapters reached.")
            break

        print(f"Scraping [{chapter_count + 1}/358]: {current_url}")
        soup = get_soup(current_url)
        if not soup:
            break

        # Extract Title
        # Title is usually in an h1 or h2. Based on subagent, it saw "Chapter 1" in h1?
        # Let's look for h1 or h3 that contains "Chapter".
        title_tag = soup.find('h1') or soup.find('h2') or soup.find('h3')
        title = title_tag.get_text(strip=True) if title_tag else f"Chapter {chapter_count + 1}"

        # Extract Content
        # Content is between the navigation buttons and the ads.
        # We can try to find the container. 
        # Common classes in WordPress/Novel themes: .entry-content, .reading-content, .text-left
        # If not found, we might need to be more heuristic.
        
        # Extract Content
        # Content is in div.text-left based on inspection
        content_div = None
        candidates = soup.find_all('div', class_='text-left')
        if candidates:
            # Pick the one with the most p tags
            content_div = max(candidates, key=lambda d: len(d.find_all('p')))
        
        if not content_div:
             # Fallback
             content_div = soup.find('div', class_='entry-content') or \
                           soup.find('div', class_='reading-content')

        content_text = ""
        if content_div:
            # Remove scripts, styles, and ads (code-block)
            for tag in content_div(["script", "style"]):
                tag.decompose()
            for div in content_div.find_all("div", class_="code-block"):
                div.decompose()
            
            content_text = content_div.get_text(separator="\n\n", strip=True)
        else:
            # Fallback: Look for text paragraphs in body if no specific container found
            paragraphs = soup.find_all('p')
            content_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])

        if not content_text:
            print("No content found, stopping.")
            break

        # Translate
        print(f"Translating {title}...")
        translated_title = translate_text(title)
        translated_content = translate_text(content_text)

        chapter_data = {
            "id": chapter_count + 1,
            "original_title": title,
            "title": translated_title,
            "content": translated_content,
            "url": current_url
        }
        chapters.append(chapter_data)
        chapter_count += 1

        # Save periodically
        if chapter_count % 1 == 0: # Save every chapter for safety
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(chapters, f, ensure_ascii=False, indent=4)

        # Find Next Link
        # Look for 'Next' button.
        # Usually <a> with text "Next" or class "next_page"
        next_link = None
        
        # Try finding by text
        next_btn = soup.find('a', string=lambda text: text and 'Next' in text)
        if not next_btn:
             # Try finding by class
             next_btn = soup.find('a', class_='next_page')
        
        if next_btn and 'href' in next_btn.attrs:
            current_url = next_btn['href']
            # Check if it's a valid URL
            if not current_url.startswith('http'):
                # Handle relative URLs if necessary (unlikely for this site)
                pass
            
            # Stop if we hit a login page or premium wall (heuristic)
            if "login" in current_url or "premium" in current_url:
                print("Next link leads to login/premium. Stopping.")
                break
        else:
            print("No next link found. Stopping.")
            break
        
        # Be polite
        time.sleep(1)
        

    print("Scraping finished.")

if __name__ == "__main__":
    scrape_novel()
