""" 
Basic example of scraping pipeline using SmartScraper
"""

import os, json
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperMultiGraph

load_dotenv()

# ************************************************
# Define the configuration for the graph
# ************************************************

groq_key = os.getenv("GROQ_APIKEY")

graph_config = {
    "llm": {
        "model": "groq/llama3-8b-8192",
        "api_key": groq_key,
        "temperature": 0
    },
    "verbose": True,
    "headless": False
}
# *******************************************************
# Create the SmartScraperMultiGraph instance and run it
# *******************************************************

multiple_search_graph = SmartScraperMultiGraph(
    prompt="This website contains reviews of Fastweb. Extract the reviews with review title, review text and review score.",
    source= [
        "https://www.indeed.com/cmp/Fastweb/reviews?fcountry=IT&lang=it&start=0",
        #"https://www.indeed.com/cmp/Fastweb/reviews?fcountry=IT&lang=it&start=20",
        #"https://www.indeed.com/cmp/Fastweb/reviews?fcountry=IT&lang=it&start=40",
        ],
    schema=None,
    config=graph_config
)

result = multiple_search_graph.run()
# ************************************************
# Get graph execution info
# ************************************************

print(result)