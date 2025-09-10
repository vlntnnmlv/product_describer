import os
import argparse

from dataclasses import dataclass

@dataclass
class Config:
    # API Parameters
    OPENAI_API_KEY: str
    MODEL_NAME: str

    # Generation parameters
    KEYWORD_COUNT: int
    DESCRIPTION_MAX_LENGTH: int

    # Processing parameters
    CHUNKSIZE: int

    # IO parameters
    INPUT_CSV_PATH: str
    OUTPUT_CSV_PATH: str

    @classmethod
    def Load(cls, args: argparse.Namespace):
        return cls(
            OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY"),
            MODEL_NAME = args.model or os.environ.get("MODEL_NAME"),

            KEYWORD_COUNT = args.keywords_count or int(os.environ.get("KEYWORD_COUNT", 3)),
            DESCRIPTION_MAX_LENGTH = args.description_length or int(os.environ.get("DESCRIPTION_MAX_LENGTH", 200)),

            CHUNKSIZE = args.chunksize or int(os.environ.get("CHUNKSIZE", 50)),

            INPUT_CSV_PATH = args.input or os.environ.get("INPUT_CSV_PATH", "input.csv"),
            OUTPUT_CSV_PATH = args.output or os.environ.get("OUTPUT_CSV_PATH", "output.csv"),
        )