from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_json
from bs4 import BeautifulSoup

class FedSanFranciscoScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-SANFRANCISCO')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url = 'https://www.frbsf.org/wp-json/wp/v2/sffed_publications?publication-type=1979&per_page=10'
        # Send request, parse response as json
        response = request_json(method = 'GET', url = url, headers = self.headers)
        
        # Initialize `data`
        data = []
        # Loop through all working paper entries from parsed JSON response
        for wp in response:
            # Title
            title = wp['title']['rendered']

            # Link
            link = wp['link']

            # Date
            date = wp['date'].split('T')[0].strip()

            # Author
            author = wp['meta']['publication_authors']

            # Number: Combine the volume and issue with a hyphen
            number = (wp["meta"]["publication_volume"].strip() 
                      + "-" 
                      + wp["meta"]["publication_issue"].strip())

            # Abstract: To retrieve, the object must be parsed using BeautifulSoup.
            # This does not entail a network request, but simply parsing HTML surrounding
            # the JSON entry.
            # First get the abstract in its raw form
            abstract_raw = wp['content']['rendered']
            # Then parse it with BeautifulSoup to parse the HTML
            abstract_html = BeautifulSoup(abstract_raw, 'html.parser')
            # Keep only text within the first <p> tag. (Sometimes there is a second 
            # <p> tag, usually containing information about how to 
            # download the pdf appendix).
            abstract_text = abstract_html.find('p').text.strip()

            data.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Author': author,
                'Number': number,
                'Abstract': abstract_text
            })

        return data



