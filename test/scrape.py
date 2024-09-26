import os
import dotenv
from firecrawl import FirecrawlApp  # Importing the FireCrawlLoader
import json

dotenv.load_dotenv()

url = """https://www.indeed.com/cmp/Fastweb/reviews?fcountry=IT&lang=it&start=60"""

firecrawl = FirecrawlApp(
    api_key=os.getenv("FIRECRAWL_APIKEY")  # Your FireCrawl API key,
)
page_content = firecrawl.scrape_url(url=url, params={'formats': ['markdown']})['markdown']
page_content = page_content.replace("\n", ". ")
page_content = page_content.replace("\"", "")
with open("page_content.txt", "w") as f:
    f.write(json.dumps(page_content, indent=4))

import json
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_APIKEY"),  # Note: Replace 'API_KEY' with your actual Groq API key
)

# Here we define the fields we want to extract from the page content
extract = ["review_title","review_body"]

completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": "You are a scraping bot that extracts reviews from documents in JSON. Generate the response JSON in a SINGLE LINE. Do not indent the JSON. Do not go to new lines. Do not add any extra characters. Do not escape characters. Do not add any extra spaces. DO NOT IGNORE THIS: The return object must be \{reviews\:[\{'review_title':'value', 'review_body':'value'\},\{'review_title':'value', 'review_body':'value'\},]\}"
        },
        {
            "role": "user",
            # Here we pass the page content and the fields we want to extract
            "content": f"Extract the reviews from the provided documentation:\Page content:\n\n{page_content}\n\The informations that i want to extract are: {extract}.\nIf you find missing information, please provide a placeholder."
        }
    ],
    temperature=0,
    max_tokens=8192,
    top_p=1,
    stream=False,
    stop=None,
    # We set the response format to JSON object
    response_format={"type": "json_object"}
)

print("_-------------------_")
# Pretty print the JSON response
dataExtracted = json.dumps(str(completion.choices[0].message.content), indent=4)

# Decode the JSON string
decoded_content = json.loads(str(completion.choices[0].message.content))

# Print the decoded JSON with proper formatting
dataExtracted = json.dumps(decoded_content, indent=4, ensure_ascii=False)

print(dataExtracted)