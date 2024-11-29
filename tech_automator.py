import os
import random
from datetime import datetime
import requests
import json
from git import Repo
import openai
from pathlib import Path
import yaml
from bs4 import BeautifulSoup

class TechNewsAutomator:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
    def get_tech_news(self):
        """Fetch real tech news headlines to use as inspiration"""
        url = f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={self.news_api_key}"
        response = requests.get(url)
        return response.json().get('articles', [])[:5]
    
    def generate_article(self, topic):
        """Generate a full article using AI"""
        openai.api_key = self.openai_key
        prompt = f"Write a detailed tech news article about {topic}. Include quotes and technical details."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def create_new_page(self):
        """Create a new page with unique content"""
        topics = ['AI', 'Cybersecurity', 'Cloud Computing', 'Mobile Tech', 'Gaming']
        page_type = random.choice([
            'tutorial', 'news', 'analysis', 'review', 'comparison'
        ])
        
        topic = random.choice(topics)
        content = self.generate_article(f"{page_type} about {topic}")
        
        filename = f"{page_type}-{topic.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.html"
        self.write_page(filename, content, page_type.title(), topic)
        return filename

    def update_index(self):
        """Update the main index page with new content and links"""
        articles = []
        for html_file in Path(self.repo_path).glob('*.html'):
            if html_file.name != 'index.html':
                with open(html_file, 'r') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    title = soup.find('h1').text
                    summary = soup.find('meta', {'name': 'description'})['content']
                    articles.append({
                        'title': title,
                        'file': html_file.name,
                        'date': html_file.stem.split('-')[-1],
                        'summary': summary
                    })
        
        articles.sort(key=lambda x: x['date'], reverse=True)
        self.write_index_page(articles[:10])  # Show last 10 articles

    def write_page(self, filename, content, page_type, topic):
        """Write content to a new HTML page"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Latest {page_type} about {topic} in tech">
            <title>{topic} {page_type} - TechDaily</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <header>
                <nav>
                    <a href="index.html">Home</a>
                    <a href="#news">News</a>
                    <a href="#tutorials">Tutorials</a>
                    <a href="#analysis">Analysis</a>
                </nav>
            </header>
            <main>
                <article>
                    <h1>{topic} {page_type}</h1>
                    <div class="metadata">
                        <span>Published: {datetime.now().strftime('%B %d, %Y')}</span>
                        <span>Category: {topic}</span>
                    </div>
                    <div class="content">
                        {content}
                    </div>
                </article>
            </main>
            <footer>
                <p>© {datetime.now().year} TechDaily - Updated Daily</p>
            </footer>
        </body>
        </html>
        """
        
        with open(os.path.join(self.repo_path, filename), 'w') as f:
            f.write(html_content)

    def update_styles(self):
        """Occasionally update the CSS styles"""
        if random.random() < 0.2:  # 20% chance to update styles
            colors = [
                '#1a73e8', '#ea4335', '#34a853', '#fbbc05',  # Google-inspired
                '#0a66c2', '#00a0dc', '#313335',  # LinkedIn-inspired
                '#1da1f2', '#14171a', '#657786'   # Twitter-inspired
            ]
            accent_color = random.choice(colors)
            
            css_content = f"""
            :root {{ --accent-color: {accent_color}; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            header {{
                background: var(--accent-color);
                color: white;
                padding: 1rem;
            }}
            nav a {{
                color: white;
                text-decoration: none;
                margin-right: 1rem;
            }}
            main {{
                max-width: 800px;
                margin: 2rem auto;
                padding: 0 1rem;
            }}
            article {{
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .metadata {{
                color: #666;
                margin-bottom: 1rem;
            }}
            .metadata span {{
                margin-right: 1rem;
            }}
            footer {{
                text-align: center;
                padding: 2rem;
                background: #f5f5f5;
            }}
            """
            
            with open(os.path.join(self.repo_path, 'style.css'), 'w') as f:
                f.write(css_content)

    def commit_and_push(self):
        """Commit and push changes to GitHub"""
        git = self.repo.git
        git.add('.')
        commit_types = ['Update', 'Add', 'Revise', 'Improve', 'Enhance']
        commit_msg = f"{random.choice(commit_types)} daily content: {datetime.now().strftime('%Y-%m-%d')}"
        git.commit('-m', commit_msg)
        git.push('origin', 'main')

def main():
    REPO_PATH = "/path/to/your/repo"  # Replace with your repo path
    automator = TechNewsAutomator(REPO_PATH)
    
    # Create new content
    new_page = automator.create_new_page()
    
    # Maybe update styles
    automator.update_styles()
    
    # Update index page
    automator.update_index()
    
    # Commit and push changes
    automator.commit_and_push()

if __name__ == "__main__":
    main()