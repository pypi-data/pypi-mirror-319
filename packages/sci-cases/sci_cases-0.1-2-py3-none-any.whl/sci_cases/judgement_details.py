import requests
import bs4
import json

session = requests.Session()

def parse_judgement_details(html_content):
    """
    Parse the HTML content to extract judgment details into a JSON object.
    """
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    cause_data = soup.find(class_="Cause-data")
    
    judgement_details = {}

    if cause_data:
        # Extract table data
        tables = cause_data.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].string.strip().replace(':', '')
                    value = cols[1].string.strip()
                    judgement_details[key] = value

        # Extract headnote text
        headnote_text = cause_data.find(class_="read-more").text
        judgement_details['Headnote'] = headnote_text.strip()    

    return json.dumps(judgement_details, indent=4)

def get_judgement(judgment_id):
    """
    Fetch judgment details using the given judgment ID.
    """
    response = session.get(f"https://digiscr.sci.gov.in/view_judgment?id={judgment_id}")
    
    # Extract relevant judgment details from the page
    judgement_details = parse_judgement_details(response.text)

    return judgement_details