import requests
import csv
import re
import argparse
from typing import List, Dict, Optional

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "50"
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_id: str) -> Dict:
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    return response.text

def extract_authors_and_affiliations(xml_text: str) -> Dict:
    company_keywords = ["pharma", "biotech", "inc", "ltd", "gmbh", "s.a.", "corp"]
    author_pattern = re.compile(r'<AuthorList>(.*?)</AuthorList>', re.DOTALL)
    email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

    authors = []
    companies = []
    corresponding_email = None

    for match in author_pattern.findall(xml_text):
        for author in re.findall(r'<Author>(.*?)</Author>', match, re.DOTALL):
            name_match = re.search(r'<LastName>(.*?)</LastName>', author)
            name = name_match.group(1) if name_match else "Unknown"

            affil_match = re.search(r'<Affiliation>(.*?)</Affiliation>', author)
            affiliation = affil_match.group(1) if affil_match else "Unknown"

            if any(keyword in affiliation.lower() for keyword in company_keywords):
                authors.append(name)
                companies.append(affiliation)

    email_match = email_pattern.search(xml_text)
    if email_match:
        corresponding_email = email_match.group(1)

    return {
        "authors": authors,
        "companies": companies,
        "email": corresponding_email
    }

def save_to_csv(data: List[Dict], filename: str):
    keys = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Fetch and filter PubMed papers.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", help="Output CSV file name")

    args = parser.parse_args()
    pubmed_ids = fetch_pubmed_ids(args.query)
    
    results = []
    for pubmed_id in pubmed_ids:
        xml_text = fetch_paper_details(pubmed_id)
        details = extract_authors_and_affiliations(xml_text)

        results.append({
            "PubmedID": pubmed_id,
            "Title": "N/A",
            "Publication Date": "N/A",
            "Non-academic Author(s)": ", ".join(details["authors"]),
            "Company Affiliation(s)": ", ".join(details["companies"]),
            "Corresponding Author Email": details["email"] or "N/A"
        })

    if args.file:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        for res in results:
            print(res)

if __name__ == "__main__":
    main()
