# News Aggregator

This project is a news aggregator that fetches news articles from various RSS feeds, stores them in a MySQL database, and processes the articles to extract topics and named entities. It includes features for filtering articles and avoiding duplicate entries.

## Features

- Fetch news articles from configurable RSS feed URLs
- Store articles in a MySQL database
- Extract topics and named entities from article content using spaCy and Google ML Services (Seperated py file)
- Filter articles based on keywords or publication dates
- Avoid duplicate entries in the database
- Periodically fetch and process new articles

## Requirements

- Python 3.x
- MySQL
- Libraries: `feedparser`, `mysql-connector-python`, `schedule`, `requests`, `beautifulsoup4`, `spacy`, `pyyaml`, `google-cloud-language`, `flask`, `plotly`, `pandas`, `python-dateutil`

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ripon23/news_aggregator.git
    cd news-aggregator
    ```

2. **Create and activate virtual env(Optional):**

    ```sh
    python -m venv venv
    . ./venv/bin/activate
    ```

3. **Install the required Python packages**:
    ```
    pip install -r requirements.txt
    ```
4. **Download the spaCy NLP model**:
    ```sh
    python -m spacy download en_core_web_sm
    ```

5. **Create and configure the MySQL database**:
    ```sql
    CREATE DATABASE rss_feed_news;
    ```

6. **Update the database credentials** in the script if necessary:
    ```python
    conn = mysql.connector.connect(
        host='localhost',
        user='your_user',
        password='your_password',
        database='rss_feed_news'
    )
    ```

7. **Create a `config.yml` file** to specify the RSS feed URLs:
    ```yaml
    feeds:
      urls:
        - 'http://feeds.bbci.co.uk/news/rss.xml'
        - 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    ```

## Usage


7. **Run the script** to fetch and process articles:

    Topics generation using Spacy:

    ```sh
    python rss_feed_spacy.py
    ```

    Topics generation using Google Service (Required google_service_account_key.json):
   
   ```sh
    python rss_feed_google_service.py
    ```


## Code Overview

### Initialization

The `init_db` function initializes the MySQL database by creating the `articles` table if it does not exist.

### Fetching Articles

The `fetch_articles` function retrieves articles from the specified RSS feed URLs using the `feedparser` library.

### Storing Articles

The `store_articles` function stores the fetched articles in the MySQL database, avoiding duplicates by checking if an article with the same title and publication date already exists. For visualization I use python flask framework.

### Extracting Topics and Named Entities

The `extract_topics_and_entities` function uses the spaCy library(rss_feed_spacy.py) and Google Service(rss_feed_google_service.py) to extract topics and named entities from the article content.

### Filtering Articles

The `filter_articles` function allows filtering of stored articles based on keywords or publication dates (Flask).

### Periodic Fetching

The script uses the `schedule` library to periodically (1 hour) fetch and process new articles from the RSS feeds.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Compariason Spacy Vs Google Service
    Case-1: 
    ---------
    News Desc: The US president announces more military aid for Ukraine, warning "autocrats have overturned global order".

    Topics(Google ML Services): military aid, president, US, order, Ukraine, autocrats
    Topics(Spacy): president, announce, military, aid, Ukraine, warn, autocrat, overturn, global, order

## Visualization using flask

   ```sh
   python app.py
   ```

* Running on http://127.0.0.1:5000

## Create google service point account: 
    https://console.cloud.google.com/apis/credentials

## Reach out me for any query:
    riponmailbox@gmail.com