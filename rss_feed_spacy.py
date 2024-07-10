import feedparser
import mysql.connector
import schedule
import time
import requests
from bs4 import BeautifulSoup
import spacy
from datetime import datetime
import yaml

# Initialize spaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Database setup
def init_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='rss_feed_news'
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      title TEXT,
                      description TEXT,
                      pub_date TEXT,
                      source_url TEXT,
                      topics TEXT,
                      named_entities TEXT
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

# Fetch articles from RSS feeds
def fetch_articles(feed_urls):
    articles = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get('title', 'No title')
                description = entry.get('description', 'No description')
                pub_date = entry.get('published', 'No date')
                source_url = entry.get('link', 'No URL')
                articles.append({
                    'title': title,
                    'description': description,
                    'pub_date': pub_date,
                    'source_url': source_url
                })
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
    return articles

# Extract topics and named entities using spaCy
def extract_topics_and_entities(text):
    doc = nlp(text)
    topics = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return topics, named_entities

# Check if article exists in the database
def article_exists(cursor, title, pub_date):
    query = "SELECT COUNT(*) FROM articles WHERE title = %s AND pub_date = %s"
    cursor.execute(query, (title, pub_date))
    count = cursor.fetchone()[0]
    return count > 0

# Store articles in the database
def store_articles(articles):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='rss_feed_news'
    )
    cursor = conn.cursor()
    for article in articles:
        title = article['title']
        description = article['description']
        pub_date = article['pub_date']
        source_url = article['source_url']
        
        # Check if the article already exists
        if article_exists(cursor, title, pub_date):
            print(f"Skipping duplicate article: {title}")
            continue
        
        topics, named_entities = extract_topics_and_entities(description)
        #print(f"Description: {description} Topics:{topics}")
        cursor.execute('''INSERT INTO articles (title, description, pub_date, source_url, topics, named_entities)
                          VALUES (%s, %s, %s, %s, %s, %s)''', 
                          (title, description, pub_date, source_url, str(topics), str(named_entities)))
    conn.commit()
    cursor.close()
    conn.close()

# Filter articles based on keywords or publication date
def filter_articles(keyword=None, start_date=None, end_date=None):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='rss_feed_news'
    )
    cursor = conn.cursor()
    query = "SELECT * FROM articles WHERE 1=1"
    params = []

    if keyword:
        query += " AND (title LIKE %s OR description LIKE %s)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")
    
    if start_date:
        query += " AND pub_date >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND pub_date <= %s"
        params.append(end_date)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Fetch and process articles periodically
def job(feed_urls):
    articles = fetch_articles(feed_urls)
    store_articles(articles)

if __name__ == "__main__":
    init_db()

    # Load feed URLs from the YAML configuration file
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
        feed_urls = config['feeds']['urls']
    
    # Fetch and process articles immediately
    job(feed_urls)

    # Schedule the job to run every hour
    schedule.every(1).hours.do(job, feed_urls)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
