import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import time

def find(filename: str):
    def scan_directory(directory, filename):
        try:
            matches = []
            with os.scandir(directory) as entries:
                for entry in entries:
                    try:
                        if entry.is_file() and entry.name.startswith(filename):
                            matches.append(entry.path)
                        elif entry.is_dir():
                            matches.extend(scan_directory(entry.path, filename))
                    except (PermissionError, OSError):
                        continue
            return matches
        except (PermissionError, OSError):
            return []

    def parallel_search(filename):
        cpu_count = multiprocessing.cpu_count()
        root_dirs = [d for d in Path(os.path.abspath(os.sep)).iterdir() 
                    if d.is_dir() and not d.is_symlink()]
        
        with ThreadPoolExecutor(max_workers=cpu_count * 2) as executor:
            start_time = time.time()
            futures = [
                executor.submit(scan_directory, str(root_dir), filename)
                for root_dir in root_dirs
            ]
            
            results = []
            for future in as_completed(futures):
                try:
                    results.extend(future.result())
                except Exception:
                    continue

            end_time = time.time()
            print(f"Search took {end_time - start_time} seconds.")
                    
        return results

    results = parallel_search(filename)
    
    if not results:
        return None
    elif len(results) == 1:
        return results[0]
    else:
        return results

