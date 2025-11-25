# Walkthrough - Novel Reader Website

I have successfully created a website to read "Chronicles of the Lazy Sovereign" in Indonesian.

## Accomplishments

- **Scraper**: Created a robust scraper ([scraper.py](file:///home/rodwell/Documents/Novel/scraper.py)) that fetches chapters from `levelingods.shop`.
  - Handles dynamic content loading.
  - Translates content from English to Indonesian using `deep-translator`.
  - Saves data to [novel_data.json](file:///home/rodwell/Documents/Novel/novel_data.json).
- **Backend**: Built a Flask application ([app.py](file:///home/rodwell/Documents/Novel/app.py)) to serve the content.
- **Frontend**: Designed a clean, dark-mode interface for comfortable reading.
  - [index.html](file:///home/rodwell/Documents/Novel/templates/index.html): Chapter list.
  - [chapter.html](file:///home/rodwell/Documents/Novel/templates/chapter.html): Reading view with navigation.
  - [style.css](file:///home/rodwell/Documents/Novel/static/style.css): Responsive and aesthetic styling.

## Verification Results

### Scraper

The scraper successfully fetched and translated 5 chapters (limited for testing).

- **Source**: https://levelingods.shop/novel/chronicles-of-the-lazy-sovereign-novel/
- **Output**: [novel_data.json](file:///home/rodwell/Documents/Novel/novel_data.json) containing 5 chapters.

### Website

The website is running locally at `http://127.0.0.1:5000`.

#### Homepage

Displays the novel title and list of chapters.
![Homepage](/home/rodwell/.gemini/antigravity/brain/6ab86f02-86e1-43b6-a934-03add822f47a/verify_website_1763991515507.webp)

#### Chapter Reading

Displays the translated content with "Next" and "Previous" navigation.
(See recording above for navigation demo)

## Static Site Generation (GitHub Pages)
I have converted the project to a static site generator to support GitHub Pages.
- **Build Script**: [build.py](file:///home/rodwell/Documents/Novel/build.py) generates static HTML files in the `docs/` folder.
- **Output**: [docs/index.html](file:///home/rodwell/Documents/Novel/docs/index.html) and `docs/chapter/*.html`.

### How to Deploy to GitHub Pages
1. **Push to GitHub**:
   Push the entire project to a GitHub repository.
2. **Configure Settings**:
   - Go to Repository Settings > Pages.
   - Under **Build and deployment**, select **Source** as `Deploy from a branch`.
   - Select **Branch** as `main` and folder as `/docs`.
   - Click **Save**.
3. **Visit Site**:
   Your site will be live at `https://<username>.github.io/<repo-name>/`.

## How to Run Locally
1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```
2. **Run Scraper** (Optional):
   ```bash
   python scraper.py
   ```
3. **Build Static Site**:
   ```bash
   python build.py
   ```
4. **View Static Site**:
   Open `docs/index.html` in your browser.
