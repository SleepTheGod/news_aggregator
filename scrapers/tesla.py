import requests
from bs4 import BeautifulSoup

def get_tesla_news():
    try:
        url = 'https://news.google.com/search?q=tesla'
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        for item in soup.find_all('div', class_='xrnccd'):
            title = item.find('h3').text
            link = item.find('a', href=True)['href']
            articles.append({
                'title': title,
                'link': 'https://news.google.com' + link,
                'source': 'Google News'
            })
        
        return articles
    except Exception as e:
        print(f"Error fetching Tesla news: {e}")
        return []
