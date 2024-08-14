from exa_py import Exa  
from crewai_tools import BaseTool
from dotenv import load_dotenv
import time
import os
from groq import Groq

load_dotenv()

exa = Exa(api_key=os.environ.get("EXA_API_KEY"))


def summary(text: str):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
                    {"role": "system", "content": """Task: As a Senior Data Engineer, provide a summary of the following text in exactly 3 lines.
                                                     Important: Your response must be only the 3-line summary, with no additional text or introductions."""},
                    {"role": "user", "content": f"{text}"}
                ],
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

    return chat_completion.choices[0].message.content


class GetWebsiteContent(BaseTool):
    name: str = "Get Website Content"
    description: str = (
        "This tool you pass only the URL of the article and it returns the Title, Published Date and a Summary of the Article"
    )

    def _run(self, article_url: str) -> str:

        result = exa.get_contents(
        [article_url],
        text={
            "max_characters": 4000
        }
        ).results[0]

        time.sleep(2)
        
        return {"title": result.title,
                "url": result.url,
                "published_date": result.published_date,
                "description": summary(result.text)}


