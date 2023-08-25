import csv
from typing import List

from fastapi import HTTPException, UploadFile


def validate_csv_headers(file: UploadFile, expected_headers: List[str]) -> bool:
    """
    Validate CSV file headers

    Args:
        file: UploadFile object
        expected_headers: List of expected headers

    Returns:
        bool: True if headers match expected headers, False otherwise

    Raises:
        HTTPException: If the provided CSV file is not UTF-8 encoded.
    """
    try:
        chunk = file.file.read(1024).decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400, detail="The provided CSV file is not UTF-8 encoded."
        )

    file.file.seek(0)  # reset pointer back to beginning

    reader = csv.DictReader(chunk.splitlines())
    headers = reader.fieldnames if reader.fieldnames else []

    return set(expected_headers) - {"id", "created_at"} == set(headers)
