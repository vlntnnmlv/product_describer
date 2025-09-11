import argparse
import asyncio

from dotenv import load_dotenv

from config import Config
from client import Client, AsyncClient
from processor import run, run_async

def main() -> None:
    parser = argparse.ArgumentParser(description = "Product describer - generate short descriptions & keywords from product names.")
    parser.add_argument("--input", "-i", required = True, help = "Path to CSV file to process")
    parser.add_argument("--output", "-o", help = "Path to output CSV file (default: output.csv)")
    parser.add_argument("--chunksize", "-c", help = "How manu products will fit in one request to AI")
    parser.add_argument("--description_length", "-d", help = "Maximum length of product descripton")
    parser.add_argument("--keywords_count", "-k", help = "Amount of keywords for a product")
    parser.add_argument("--model", "-m", help = "Name of the model")
    parser.add_argument("--async", "-a", help = "Turnon asynchronouse mode")

    args = parser.parse_args()

    load_dotenv()
    config = Config.Load(args)
    client = AsyncClient(config)
    asyncio.run(run_async(client, config))

if __name__ == "__main__":
    from time import perf_counter
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"Elapsed time: {end - start}")
