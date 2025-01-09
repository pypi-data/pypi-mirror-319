# filtertree

Apply a filter to the directory tree.

## Install

filtertree can be installed with pip:

    $ pip install filtertree

## Usage

filtertree module provides a function `filtertree`.

```python
from filtertree import filtertree

filtertree(func, src_dir_path, dest_dir_path, overwrite=overwrite)
```

Arguments are:

- `func` is a filter function that takes 2 arguments, source and destination file paths.
- `src_dir_path` is a base directory path for source.
- `dest_dir_path` is a base directory path for destination.
- `overwrite` is a flag to overwrite destination files.

`filtertree` function applies `func` to each file under `src_dir_path` directory tree and the same location under `dest_dir_path`.

If `overwrite` is `True`, overwrite the destination files, Or not. Default to `False`.

## CLI tool `filtre`

`filtre` applies command to `src_dir` directory tree as follows:

    $ filtre src_dir dest_dir cp

Or you can give one-line-script with `-c` option.

    $ filtre -c "cp $1 $2" src_dir dest_dir

`$1` and `$2` in one-lien-script are replaced by src and dest file paths.

If `-o` / `--overwite` option is passed, overwrite the destination files. Otherwise, skip.

## License

MIT license.
