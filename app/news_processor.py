import requests
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import openai
from .config import Config
from .utils import clean_text, validate_date

class NewsProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.news_api_key = Config.NEWS_API_KEY
        self.openai_key = Config.OPENAI_KEY
        openai.api_key = self.openai_key

    def fetch_news(self, date, district):
        """Fetch news articles for given date and district"""
        from_date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        to_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        query = f"{district} police OR crime OR arrest"
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&sortBy=popularity&apiKey={self.news_api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            return [{
                'title': clean_text(article['title']),
                'description': clean_text(article['description']),
                'content': clean_text(article['content']),
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'source': {'name': article['source']['name']}
            } for article in articles if article['title'] and article['description']]
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def find_related_historical(self, cluster_text, district):
        """Find related articles from past 7 days"""
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        articles = self.fetch_news(week_ago, district)
        
        if not articles:
            return []
        
        # Compare embeddings
        cluster_embedding = self.model.encode(cluster_text)
        article_embeddings = self.model.encode([a['content'] for a in articles])
        
        # Calculate similarity scores
        similarities = np.dot(article_embeddings, cluster_embedding)
        top_indices = similarities.argsort()[-3:][::-1]  # Get top 3 matches
        
        return [articles[i] for i in top_indices if similarities[i] > 0.5]

    def generate_summary(self, articles):
        """Generate AI summary for a cluster of articles"""
        if not articles:
            return "No summary available"
            
        content = "\n".join([f"{a['title']}: {a['description']}" for a in articles])
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a police analyst summarizing crime incidents. Be concise and factual."
                }, {
                    "role": "user",
                    "content": f"Summarize these related crime reports in 2-3 sentences:\n{content}"
                }]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Summary unavailable"

    def cluster_articles(self, articles):
        """Cluster similar articles using embeddings"""
        if not articles:
            return []
            
        texts = [f"{a['title']} {a['description']}" for a in articles]
        embeddings = self.model.encode(texts)
        
        # Determine optimal clusters (max 5)
        n_clusters = min(5, max(1, len(articles) // 3))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(embeddings)
        
        clusters = []
        for i in range(n_clusters):
            cluster_articles = [articles[j] for j in range(len(articles)) if kmeans.labels_[j] == i]
            combined_text = " ".join([a['content'] for a in cluster_articles])
            clusters.append({
                'articles': cluster_articles,
                'historical': self.find_related_historical(combined_text, "Mumbai Police"),
                'summary': self.generate_summary(cluster_articles)
            })
        
        return clusters

def process_news(date, district):
    """Main function to process news for given date and district"""
    if not validate_date(date):
        raise ValueError("Invalid date format")
        
    processor = NewsProcessor()
    articles = processor.fetch_news(date, district)
    if not articles:
        return []
    
    return processor.cluster_articles(articles)