from flask import Flask, render_template
from config import Config
from models import db, NewsArticle
from scrapers.spacex_scraper import get_spacex_news
from scrapers.tesla_scraper import get_tesla_news
from scrapers.fcc_scraper import get_fcc_news
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Function to update news articles in the database
def update_news():
    try:
        spacex_news = get_spacex_news()
        tesla_news = get_tesla_news()
        fcc_news = get_fcc_news()

        # Merge articles into the database to avoid duplicates
        for article in spacex_news:
            db.session.merge(NewsArticle(title=article['title'], link=article['link'], source='SpaceX'))
        
        for article in tesla_news:
            db.session.merge(NewsArticle(title=article['title'], link=article['link'], source='Tesla'))
        
        for article in fcc_news:
            db.session.merge(NewsArticle(title=article['title'], link=article['link'], source='FCC'))
        
        db.session.commit()
        print("News articles updated successfully.")
    except Exception as e:
        print(f"Error updating news: {e}")
        db.session.rollback()

# Start scheduler to scrape every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_news, trigger="interval", minutes=30)
scheduler.start()

@app.route('/')
def dashboard():
    articles = NewsArticle.query.order_by(NewsArticle.timestamp.desc()).all()
    return render_template('dashboard.html', articles=articles)

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    scheduler.shutdown()

if __name__ == '__main__':
    app.run(debug=True)
