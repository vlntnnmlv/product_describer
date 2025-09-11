from typing import Any, Generator
import pandas as pd
import asyncio

from tqdm import tqdm

from client import Client, AsyncClient
from config import Config
from prompt import build_batch_prompt
from parser import parse_batch_response

def get_num_chunks(df: pd.DataFrame, chunksize: int) -> int:
    return (len(df) + chunksize - 1) // chunksize

def dataframe_iterator(df: pd.DataFrame, chunksize: int):
    num_chunks = get_num_chunks(df, chunksize)
    for i in range(num_chunks):
        start_index = i * chunksize
        end_index = min((i + 1) * chunksize, len(df))
        yield df.iloc[start_index : end_index]

class Processor:
    def __init__(self, config: Config):
        self.config = config
        self.results = []
        self.__init_client()

    def __init_client(self):
        self.client = AsyncClient(self.config) if self.config.ASYNC else Client(self.config)

    def run(self):
        df = pd.read_csv(self.config.INPUT_CSV_PATH)
        df_iterator = dataframe_iterator(df, self.config.CHUNKSIZE)

        self.results = []
        print(f"""Chunksize: {self.config.CHUNKSIZE}
To process:
    - {len(df)} products
    - {get_num_chunks(df, self.config.CHUNKSIZE)} chunks
""")
        if type(self.client) is Client:
            self.run_sync(df, df_iterator)
        else:
            asyncio.run(self.run_async(df, df_iterator))

        df_result = pd.DataFrame(self.results)
        df_result.to_csv(self.config.OUTPUT_CSV_PATH, sep=',', encoding='utf-8', index=False, header=True)

    def run_sync(self, df: pd.DataFrame, df_iterator: Generator[pd.DataFrame, Any, None]):
        for chunk in tqdm(df_iterator, total = get_num_chunks(df, self.config.CHUNKSIZE), desc = "Processing chunks"):
            chunk_size = len(chunk)
            prompt = build_batch_prompt(chunk["product"], self.config.KEYWORD_COUNT, self.config.DESCRIPTION_MAX_LENGTH)
            raw_response_object  = self.client.generate(prompt)
            error = raw_response_object.error
            if error:
                break

            raw_response = raw_response_object.output_text
            parsed_response = parse_batch_response(raw_response, chunk_size)
            for product_info in parsed_response:
                self.results.append({
                        "product" : product_info["product"],
                        "description" : product_info["description"],
                        "keywords" : ", ".join(product_info["keywords"]),
                    })

        if not error:
            print("Success")
        else:
            print("Failure")

    async def run_async(self, df, df_iterator):
        async def process_chunk(chunk: pd.DataFrame):
            prompt = build_batch_prompt(chunk["product"], self.config.KEYWORD_COUNT, self.config.DESCRIPTION_MAX_LENGTH)
            raw_response_object = await self.client.generate(prompt)
            raw_response = raw_response_object.output_text

            if raw_response_object.error:
                return None

            parsed_response = parse_batch_response(raw_response, len(chunk))
            return [{
                "product" : product_info["product"],
                "description" : product_info["description"],
                "keywords" : ", ".join(product_info["keywords"]), 
            } for product_info in parsed_response]

        tasks = [process_chunk(chunk) for chunk in df_iterator]
        for chunk_results in tqdm(asyncio.as_completed(tasks), total = get_num_chunks(df, self.config.CHUNKSIZE), desc = "Processing chunks"):
            awaited_result = await chunk_results
            if not awaited_result:
                continue

            self.results.extend(awaited_result)
