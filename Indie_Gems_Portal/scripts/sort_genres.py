# File: process_genres.py

import json
import os
from typing import List, Dict, Any

def read_and_sort_genres(file_path: str, n: int) -> List[Dict[str, Any]]:
    # Load the JSON data from genres.ts
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Find the starting point of the JSON data, since this is wrapped in export default
        json_start = content.find('[')
        if json_start == -1:
            raise ValueError("Failed to find JSON data start in the file")

        # Trim the exported variable to get only the JSON part
        json_data = content[json_start:]

        # Convert string into a Python list of dictionaries
        genres = json.loads(json_data)

    # Sort the genres by the 'games_count' field in descending order
    sorted_genres = sorted(genres, key=lambda x: x.get('games_count', 0), reverse=True)

    # Return the first n objects
    return sorted_genres[:n]