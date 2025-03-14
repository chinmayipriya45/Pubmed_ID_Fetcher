import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_ids  # Correct function name

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results (optional)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Call the correct function
    pubmed_ids = fetch_pubmed_ids(args.query)
    print("Fetched PubMed IDs:", pubmed_ids)

if __name__ == "__main__":
    main()
