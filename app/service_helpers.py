import csv
import io
from typing import List

from fastapi import UploadFile


def read_csv_in_chunks(file: UploadFile, chunk_size=1000) -> List[dict]:
    """
    Read csv in chunks
    """
    text_stream = io.TextIOWrapper(file.file)
    reader = csv.DictReader(text_stream)
    while True:
        data = [row for idx, row in enumerate(reader) if idx < chunk_size]
        if not data:
            break
        yield data
