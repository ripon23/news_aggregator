from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def fetch_articles(keyword=None, start_date=None, end_date=None):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='rss_feed_news'
    )
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

    df = pd.read_sql(query, conn, params=params)
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    conn.close()
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = request.form.get('keyword')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    articles = fetch_articles(keyword, start_date, end_date)
    articles_list = articles.to_dict('records')

    return render_template('index.html', articles=articles_list)

if __name__ == '__main__':
    app.run(debug=True)
