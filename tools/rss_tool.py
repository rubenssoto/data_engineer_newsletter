from crewai_tools import BaseTool
from model import Articles
import feedparser
from openai import OpenAI
from dotenv import load_dotenv
import os



load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class RSSFeedTool(BaseTool):
    name: str = "RSS Feed Tool"
    description: str = (
        """This tool is useful to get a list of articles from many RSS Feeds related to the data engineering field. 
           It is not needed to pass parameters"""
    )

    def _run(self) -> str:

        rss_feeds = [
            'https://duckdb.org/feed.xml',
            'https://medium.com/feed/@kohaleavin',
            'https://medium.com/feed/@radecicdario',
            'https://medium.com/feed/@mshakhomirov',
            'https://medium.com/feed/@pallavisinha12',
            'https://medium.com/feed/@pflooky',
            'https://medium.com/feed/@yousry',
            'https://www.startdataengineering.com/index.xml']

        latest_articles = []

        for feed_url in rss_feeds:
            feed = feedparser.parse(feed_url)

            if 'entries' in feed:

                articles_feed = []
                for entry in feed.entries[:5]:
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published if 'published' in entry else 'N/A',
                    }

                    articles_feed.append(article)

                completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a Senior Data Engineering Selector. 
                                                     Your task is to review the provided list of articles 
                                                     and select the two most relevant ones in the data engineering field. Only choose from 
                                                     the articles in the list, and do not introduce or consider any articles that are not included."""},
                    {"role": "user", "content": f"{articles_feed}"}
                ],
                response_format=Articles,
                temperature=0.1
                )

                for article in completion.choices[0].message.parsed.articles:

                   latest_articles.append(article.model_dump())
            
        return latest_articles
    
