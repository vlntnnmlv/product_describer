import argparse
from dotenv import load_dotenv

from config import Config
from client import Client
from processor import run

def main() -> None:
    parser = argparse.ArgumentParser(description = "Product describer - generate short descriptions & keywords from product names.")
    parser.add_argument("--input", "-i", required = True, help = "Path to CSV file to process")
    parser.add_argument("--output", "-o", help = "Path to output CSV file (default: output.csv)")
    parser.add_argument("--chunksize", "-c", help = "How manu products will fit in one request to AI")
    parser.add_argument("--description_length", "-d", help = "Maximum length of product descripton")
    parser.add_argument("--keywords_count", "-k", help = "Amount of keywords for a product")
    parser.add_argument("--model", "-m", help = "Name of the model")

    args = parser.parse_args()

    load_dotenv()
    config = Config.Load(args)
    client = Client(config)
    run(client, config)

if __name__ == "__main__":
    main()
