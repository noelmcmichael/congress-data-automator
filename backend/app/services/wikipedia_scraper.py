"""
Scrapes congressional data from Wikipedia.
"""
import httpx
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger()

class WikipediaScraper:
    """
    Scrapes data from Wikipedia pages for the 119th Congress.
    """

    def __init__(self):
        self.urls = {
            "members": "https://en.wikipedia.org/wiki/119th_United_States_Congress#Members",
            "leadership": "https://en.wikipedia.org/wiki/119th_United_States_Congress#Leadership",
            "committees": "https://en.wikipedia.org/wiki/119th_United_States_Congress#Committees",
        }

    async def fetch_page(self, url: str) -> str:
        """
        Fetches the HTML content of a given URL.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching page", url=url, error=str(e))
            raise
        except httpx.RequestError as e:
            logger.error("Request error fetching page", url=url, error=str(e))
            raise



    def parse_members(self, html: str):
        """
        Parses the members table from the Wikipedia page.
        For now, we'll focus on committee leadership rather than full membership.
        """
        # For this Wikipedia integration, we're focusing on committee leadership
        # which is more reliable and addresses the specific data accuracy issue
        return {"members": []}

    def parse_committees(self, html: str):
        """
        Parses the committees tables from the Wikipedia page.
        """
        soup = BeautifulSoup(html, 'html.parser')
        committees = []

        # Find all tables on the page
        tables = soup.find_all('table')
        
        for table in tables:
            # Check if this table has committee information
            headers = table.find_all('th')
            if len(headers) >= 3:
                header_text = [th.text.strip() for th in headers]
                
                # Look for committee-related headers
                if any(keyword in ' '.join(header_text).lower() for keyword in ['committee', 'chair', 'ranking']):
                    # Determine chamber based on context
                    chamber = "Unknown"
                    # Look for section headers above this table
                    prev_element = table.find_previous(['h2', 'h3', 'h4'])
                    if prev_element:
                        header_text = prev_element.text.strip()
                        if 'Senate' in header_text:
                            chamber = "Senate"
                        elif 'House' in header_text:
                            chamber = "House"
                        elif 'Joint' in header_text:
                            chamber = "Joint"
                    
                    # Extract committee data
                    rows = table.find_all('tr')[1:]  # Skip header row
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) >= 3:
                            committee_name = cells[0].text.strip()
                            chair = cells[1].text.strip()
                            ranking_member = cells[2].text.strip()
                            
                            # Clean up the names (remove extra formatting)
                            committee_name = committee_name.replace('\n', ' ').strip()
                            chair = chair.replace('\n', ' ').strip()
                            ranking_member = ranking_member.replace('\n', ' ').strip()
                            
                            # Only add if this looks like a real committee
                            if (len(committee_name) < 200 and 
                                len(chair) < 200 and 
                                len(ranking_member) < 200 and
                                not any(skip in committee_name.lower() for skip in ['members', 'powers', 'capitol', 'legislative']) and
                                chamber in ['Senate', 'House', 'Joint']):
                                
                                committee_data = {
                                    "name": committee_name,
                                    "chamber": chamber,
                                    "chair": chair,
                                    "ranking_member": ranking_member
                                }
                                
                                # Add joint committee specific fields
                                if chamber == "Joint" and len(cells) >= 5:
                                    committee_data["vice_chair"] = cells[2].text.strip()
                                    committee_data["vice_ranking_member"] = cells[4].text.strip()
                                
                                committees.append(committee_data)

        return {"committees": committees}

    async def scrape(self):
        """
        Scrapes all data from the Wikipedia pages.
        """
        scraped_data = {}
        
        # Scrape Members
        members_html = await self.fetch_page(self.urls["members"])
        scraped_data.update(self.parse_members(members_html))

        # Scrape Committees
        committees_html = await self.fetch_page(self.urls["committees"])
        scraped_data.update(self.parse_committees(committees_html))

        return scraped_data

if __name__ == "__main__":
    import asyncio
    scraper = WikipediaScraper()
    data = asyncio.run(scraper.scrape())
    import json
    with open("wikipedia_data.json", "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Scraped data written to wikipedia_data.json")
