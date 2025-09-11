import pandas as pd
import asyncio

from tqdm import tqdm

from client import Client, AsyncClient
from config import Config
from prompt import build_batch_prompt
from parser import parse_batch_response

class Processor:
    # TODO:
    pass

def get_num_chunks(df: pd.DataFrame, chunksize: int) -> int:
    return (len(df) + chunksize - 1) // chunksize

def dataframe_iterator(df: pd.DataFrame, chunksize: int):
    num_chunks = get_num_chunks(df, chunksize)
    for i in range(num_chunks):
        start_index = i * chunksize
        end_index = min((i + 1) * chunksize, len(df))
        yield df.iloc[start_index : end_index]

def run(client: Client, config: Config) -> None:
    df = pd.read_csv(config.INPUT_CSV_PATH)
    df_iterator = dataframe_iterator(df, config.CHUNKSIZE)

    results = []
    print(f"""Chunksize: {config.CHUNKSIZE}
To process:
    - {len(df)} products
    - {get_num_chunks(df, config.CHUNKSIZE)} chunks
""")

    for chunk in tqdm(df_iterator, total=get_num_chunks(df, config.CHUNKSIZE), desc="Processing chunks"):
        chunk_size = len(chunk)
        prompt = build_batch_prompt(chunk["product"], config.KEYWORD_COUNT, config.DESCRIPTION_MAX_LENGTH)
        error, raw_response = client.generate(prompt)
        if error:
            break

        parsed_response = parse_batch_response(raw_response, chunk_size)
        for product_info in parsed_response:
            results.append({
                    "product" : product_info["product"],
                    "description" : product_info["description"],
                    "keywords" : ", ".join(product_info["keywords"]),
                })

    if not error:
        print("Success")
    else:
        print("Failure")

    df_result = pd.DataFrame(results)
    df_result.to_csv(config.OUTPUT_CSV_PATH, sep=',', encoding='utf-8', index=False, header=True)

async def run_async(client: AsyncClient, config: Config) -> None:
    async def process_chunk(chunk: pd.DataFrame):
        prompt = build_batch_prompt(chunk["product"], config.KEYWORD_COUNT, config.DESCRIPTION_MAX_LENGTH)
        raw_response_object = await client.generate(prompt)
        raw_response = raw_response_object.output_text

        if raw_response_object.error:
            return None

        parsed_response = parse_batch_response(raw_response, len(chunk))
        return [{
            "product" : product_info["product"],
            "description" : product_info["description"],
            "keywords" : ", ".join(product_info["keywords"]), 
        } for product_info in parsed_response]

    results = []

    df = pd.read_csv(config.INPUT_CSV_PATH)
    df_iterator = dataframe_iterator(df, config.CHUNKSIZE)

    results = []
    tasks = [process_chunk(chunk) for chunk in df_iterator]
    for chunk_results in asyncio.as_completed(tasks):
        awaited_result = await chunk_results
        if not awaited_result:
            continue

        results.extend(awaited_result)

    df_result = pd.DataFrame(results)
    df_result.to_csv(config.OUTPUT_CSV_PATH, sep=',', encoding='utf-8', index=False, header=True)
