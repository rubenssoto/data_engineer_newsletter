from pydantic import BaseModel

class Article(BaseModel):
    title: str
    link: str
    published: str

class Articles(BaseModel):
    articles: list[Article]