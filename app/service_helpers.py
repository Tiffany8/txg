import csv
import logging
from typing import Dict, Generator, List

from fastapi import UploadFile
import pandas as pd

logger = logging.getLogger(__name__)


import csv
from typing import Dict, List, Generator
from fastapi import UploadFile


def read_csv_in_chunks(
    file: UploadFile, chunk_size: int = 1000
) -> Generator[List[Dict[str, str]], None, None]:
    # Use pandas' read_csv function to read the file in chunks
    chunk_iter = pd.read_csv(file.file, chunksize=chunk_size)
    for chunk_df in chunk_iter:
        # Convert each DataFrame chunk to a list of dictionaries
        chunk = chunk_df.to_dict(orient="records")
        yield chunk
