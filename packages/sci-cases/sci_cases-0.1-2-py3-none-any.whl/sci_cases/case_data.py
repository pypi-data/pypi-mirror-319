import requests
import bs4

session = requests.Session()

def fetch_case_data(
    selval="Advanced", assendings="", cause_title="", date_option="", 
    disposal_nature_value="", doj_start="", doj_end="", keyword="", 
    neutral_number="", party_type="2", scr_case_number="", volume="", 
    year="", page="1"
):
    """
    Fetch case data from the Supreme Court of India's website.
    Parameters can be adjusted to filter results.
    """

    # Prepare POST request headers and data
    request_data = {
        "selval": selval,
        "assendings": assendings,
        "cause_title": cause_title,
        "dateoption": date_option,
        "disposal_nature_value": disposal_nature_value,
        "doj1": doj_start,
        "doj3": doj_end,
        "keyword": keyword,
        "neutral_number": neutral_number,
        "part_type": party_type,
        "scr_case_no": scr_case_number,
        "scr_citation_search": "",
        "search": "search",
        "selectcition": "Citationdiv",
        "token": "9a4eff698e26d85b421775fb49163709",
        "volume": volume,
        "year": str(year),
        "page": page
    }

    response = session.post(
        "https://digiscr.sci.gov.in/filter_ajax",
        headers={
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        },
        data=request_data
    )

    return response.text

def parse_case_data(html_content):
    """
    Parse the HTML content to extract case data.
    """
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Extract case data from the response
    citations = [
        cite.find(id="neutral-cite").text.strip()
        for cite in soup.find_all(class_="cite-data")
    ]
    
    # Determine pagination details
    page_links = soup.find_all(class_="page-link")
    multiple_pages = len(page_links) > 1
    total_pages = int(page_links[-2].text) if multiple_pages else 1
    
    # Extract judgment IDs
    judgment_ids = [
        link.a['href'].replace('view_judgment?id=', '')
        for link in soup.find_all(class_="col-lg-8 col-md-12 col-12")
    ]

    # Combine citations and judgment IDs into dictionaries
    cases = [
        {"citation": citation, "judgment_id": judgment_id}
        for citation, judgment_id in zip(citations, judgment_ids)
    ]

    # Compile data into a dictionary
    case_data = {
        "cases": cases,
        "multiplePages": multiple_pages,
        "pagesNum": total_pages
    }

    return case_data

def cases_query(
    selval="Advanced", assendings="", cause_title="", date_option="", 
    disposal_nature_value="", doj_start="", doj_end="", keyword="", 
    neutral_number="", party_type="2", scr_case_number="", volume="", 
    year="", page="1"
):
    """
    Fetch and parse case data from the Supreme Court of India's website.
    """
    html_content = fetch_case_data(
        selval, assendings, cause_title, date_option, disposal_nature_value,
        doj_start, doj_end, keyword, neutral_number, party_type, scr_case_number,
        volume, year, page
    )
    
    case_data = parse_case_data(html_content)
    
    # Return the case data
    return case_data