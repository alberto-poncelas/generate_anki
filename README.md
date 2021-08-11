# generate_anki

A tool for creating an Anki deck from a file with word pairs. This tool has been built using [genanki](https://github.com/kerrickstaley/genanki) package.

Usage:

```
python3 generate_anki.py path/to/file
```

It will create an apkg file with the same name as the file.


If the file contains several columns it is possible to choose which will be in the front side of the card and which in the column. In order to do that use the `--front` and `--back` options (being 0 the first column in the file).


```
python3 generate_anki.py path/to/file --sep "\t" --front 0 2 --back 3
```


