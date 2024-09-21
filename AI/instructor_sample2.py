from typing import List, Optional

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from urllib.parse import urlparse


@lru_cache(maxsize=10)
def cached_requests_get(url):
    return requests.get(url)


def get_same_origin_links_for_llm(domain, url):

    response = cached_requests_get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags in the HTML
    links = soup.find_all('a', href=True)

    # Prepare to collect same-origin URLs
    same_origin_urls = []

    # Iterate through found links
    for link in links:
        # Parse the href attribute of each link
        href = link['href']
        parsed_href = urlparse(href)

        # Check if the domain of the href matches the input domain
        # We need to handle cases where href might be a relative URL
        if parsed_href.netloc == "" or parsed_href.netloc == domain:
            # Construct full URL if it's a relative link
            full_url = href if parsed_href.netloc else f"http://{domain}{href}"
            same_origin_urls.append(full_url)

    return same_origin_urls


def get_webpage_text_for_llm(url):
    try:
        # Retrieve the webpage content
        response = cached_requests_get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the main content of the webpage, you may need to adjust this depending on the webpage structure
        # This example attempts to generalize by focusing on body text and ignoring scripts, styles, etc.
        for script in soup(["script", "style", "header", "footer", "nav", "form"]):
            script.decompose()  # Remove these elements

        # Get text and strip whitespace
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Convert to Markdown (basic conversion here, could be expanded)
        # For simplicity, just wrap the text in a Markdown code block to preserve whitespace formatting
        markdown_text = f"```\n{text}\n```"

        return markdown_text
    except requests.RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"



class SubsidiariesExtractionResult(BaseModel):
    success: bool = Field(..., description="Indicates if the extraction was successful")
    subsidiaries: Optional[List[str]] = Field(
        default=None,
        description="A list of extracted subsidiaries",
        example=["Company A", "Company B"]  # Providing an example
    )
    additional_followup_urls: Optional[List[str]] = Field(
        default=None,
        description="A list of folllowup urls from the page that may have more subsidiary information."
                    " (anything like 'about us' page)",
    )
    error_message: Optional[str] = None  # Describe the error if success is False

    class Config:
        description = """
        This model represents the result of an attempt to extract commercial subsidiaries information.
        It includes a success flag and a list of subsidiary names if the extraction was successful.
        Subsidiaries are commercial companies that are owned or controlled by another company.
        """


def get_subsidiaries(url:str):
    client = instructor.from_openai(OpenAI())
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        # model="gpt-4",
        response_model=SubsidiariesExtractionResult,
        messages=[
            {"role": "system", "content": "You are a business analyst assistant. "
                                                "You need to extract the names of the subsidiaries of a company"
                                                " from a text document."},
            {"role": "user", "content": "Web page content:\n" + get_webpage_text_for_llm(url)},
            {"role": "user", "content": "Candidate followup urls:\n" +
                                        str(get_same_origin_links_for_llm(urlparse(url).netloc,url ))
             }
        ]
    )
    return response



# starting_url = 'https://www.cnp.fr'
starting_url = 'https://www.cnp.fr/le-groupe-cnp-assurances/qui-sommes-nous/nos-activites/cnp-assurances-dans-le-monde'


res = get_subsidiaries(starting_url)
# res = get_same_origin_links_for_llm(urlparse(starting_url).netloc, starting_url)


print(res)
