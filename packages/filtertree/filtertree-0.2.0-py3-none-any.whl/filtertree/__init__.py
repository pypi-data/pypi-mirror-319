from pathlib import Path
import os

__version__ = "0.2.0"


def filtertree(func, src_dir, dest_dir, overwrite=False):
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)
    for curr, _, files in os.walk(src_dir):
        current_dir = Path(curr)
        for file in files:
            src_file_path = current_dir / file
            dest_file_path = dest_dir / src_file_path.relative_to(src_dir)
            if dest_file_path.exists() and not overwrite:
                continue
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)
            func(src_file_path, dest_file_path)
