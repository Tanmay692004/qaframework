"""
Data Loader utilities for JSON and CSV test data.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DataLoader:
    """Helper to load test data from files in a predictable way."""

    @staticmethod
    def load_json(relative_path: str) -> Any:
        file_path = PROJECT_ROOT / relative_path
        with file_path.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)

    @staticmethod
    def load_csv(relative_path: str) -> list[dict[str, str]]:
        file_path = PROJECT_ROOT / relative_path
        with file_path.open("r", encoding="utf-8", newline="") as file_handle:
            return list(csv.DictReader(file_handle))
