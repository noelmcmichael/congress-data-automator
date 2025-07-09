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

    def parse_senate_members(self, soup: BeautifulSoup):
        """
        Parses the senate members table from the Wikipedia page.
        """
        senators = []
        senate_heading = soup.find("span", {"id": "Senate_membership"})
        if not senate_heading:
            return senators

        # Find the div containing the senate member tables
        current_element = senate_heading.find_next()
        while current_element and current_element.name != 'h3':
            if current_element.name == 'h4':
                state_name = current_element.text.strip()
                table = current_element.find_next_sibling("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) >= 2:
                            class_text = cells[0].text.strip().replace('▌', '').strip()
                            name_text = cells[1].text.strip()
                            
                            # Extract name and party
                            name_parts = name_text.split('(')
                            name = name_parts[0].strip()
                            party = name_parts[1].replace(')', '').strip() if len(name_parts) > 1 else None

                            senators.append({
                                "name": name,
                                "party": party,
                                "state": state_name,
                                "chamber": "Senate",
                                "class": class_text
                            })
            current_element = current_element.find_next()
            
        return senators

    def parse_house_members(self, soup: BeautifulSoup):
        """
        Parses the house members table from the Wikipedia page.
        """
        representatives = []
        house_heading = soup.find("span", {"id": "House_membership"})
        if not house_heading:
            return representatives

        current_element = house_heading.find_next()
        while current_element and current_element.name != 'h3':
            if current_element.name == 'h4':
                state_name = current_element.text.strip()
                ul = current_element.find_next_sibling("ul")
                if ul:
                    for li in ul.find_all("li"):
                        text = li.text.strip().replace('▌', '').strip()
                        parts = text.split('.')
                        if len(parts) > 1:
                            district = parts[0].strip()
                            name_party_part = ".".join(parts[1:]).strip()
                            
                            name_parts = name_party_part.split('(')
                            name = name_parts[0].strip()
                            party = name_parts[1].replace(')', '').strip() if len(name_parts) > 1 else None

                            representatives.append({
                                "name": name,
                                "party": party,
                                "state": state_name,
                                "chamber": "House",
                                "district": district
                            })
            current_element = current_element.find_next()

        return representatives

    def parse_members(self, html: str):
        """
        Parses the members table from the Wikipedia page.
        """
        soup = BeautifulSoup(html, 'html.parser')
        senators = self.parse_senate_members(soup)
        house_members = self.parse_house_members(soup)

        return {"members": senators + house_members}

    def parse_committees(self, html: str):
        """
        Parses the committees tables from the Wikipedia page.
        """
        soup = BeautifulSoup(html, 'html.parser')
        committees = []

        # Senate Committees
        senate_committee_heading = soup.find("span", {"id": "Senate_committees"})
        if senate_committee_heading:
            table = senate_committee_heading.find_next("table", {"class": "wikitable"})
            if table:
                rows = table.find_all("tr")[1:]  # Skip header row
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 3:
                        committee_name = cells[0].text.strip()
                        chair = cells[1].text.strip()
                        ranking_member = cells[2].text.strip()
                        committees.append({
                            "name": committee_name,
                            "chamber": "Senate",
                            "chair": chair,
                            "ranking_member": ranking_member
                        })

        # House Committees
        house_committee_heading = soup.find("span", {"id": "House_committees"})
        if house_committee_heading:
            table = house_committee_heading.find_next("table", {"class": "wikitable"})
            if table:
                rows = table.find_all("tr")[1:]  # Skip header row
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 3:
                        committee_name = cells[0].text.strip()
                        chair = cells[1].text.strip()
                        ranking_member = cells[2].text.strip()
                        committees.append({
                            "name": committee_name,
                            "chamber": "House",
                            "chair": chair,
                            "ranking_member": ranking_member
                        })

        # Joint Committees
        joint_committee_heading = soup.find("span", {"id": "Joint_committees"})
        if joint_committee_heading:
            table = joint_committee_heading.find_next("table", {"class": "wikitable"})
            if table:
                rows = table.find_all("tr")[1:] # Skip header row
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 5:
                        committee_name = cells[0].text.strip()
                        chair = cells[1].text.strip()
                        vice_chair = cells[2].text.strip()
                        ranking_member = cells[3].text.strip()
                        vice_ranking_member = cells[4].text.strip()
                        committees.append({
                            "name": committee_name,
                            "chamber": "Joint",
                            "chair": chair,
                            "vice_chair": vice_chair,
                            "ranking_member": ranking_member,
                            "vice_ranking_member": vice_ranking_member
                        })

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
