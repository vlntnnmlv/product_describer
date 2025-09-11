import argparse
import asyncio

from dotenv import load_dotenv
from time import perf_counter
from typing import Callable

from config import Config
from processor import Processor

def elapse(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Elapsed time: {end - start}")
        return result

    return wrapper

@elapse
def main() -> None:
    parser = argparse.ArgumentParser(description = "Product describer - generate short descriptions & keywords from product names.")
    parser.add_argument("--input", "-i", required = True, help = "Path to CSV file to process")
    parser.add_argument("--output", "-o", help = "Path to output CSV file (default: output.csv)")
    parser.add_argument("--chunksize", "-c", help = "How manu products will fit in one request to AI")
    parser.add_argument("--description_length", "-d", help = "Maximum length of product descripton")
    parser.add_argument("--keywords_count", "-k", help = "Amount of keywords for a product")
    parser.add_argument("--model", "-m", help = "Name of the model")
    parser.add_argument("--asynchronous", "-a", help = "Turnon asynchronouse mode")

    args = parser.parse_args()

    load_dotenv()
    config = Config.Load(args)

    processor = Processor(config)
    processor.run()

if __name__ == "__main__":
    main()
