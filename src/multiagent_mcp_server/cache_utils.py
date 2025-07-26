import hashlib
import json
import os
from typing import Dict, Any

CACHE_DIR = ".scan_cache"

def file_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def cache_result(filepath: str, result: Any):
    os.makedirs(CACHE_DIR, exist_ok=True)
    hashval = file_hash(filepath)
    cache_file = os.path.join(CACHE_DIR, f"{os.path.basename(filepath)}.{hashval}.json")
    with open(cache_file, "w") as f:
        json.dump(result, f)

def load_cached_result(filepath: str):
    hashval = file_hash(filepath)
    cache_file = os.path.join(CACHE_DIR, f"{os.path.basename(filepath)}.{hashval}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return None