# Bible MP3 Tagger

This small script can add ID3 tags to your MP3 audio bibles to put them in
"albums" for your music player app, so you can navigate more easily.

The names of the biblical books are in German, but that's not hard to edit
in `tag-mp3s.py`.

## Expected directory structure

The script needs a parameter: the directory holding your MP3 bibles.
Inside this directory (`ROOT` below), the following structure is expected
(either one MP3 per book or per chapter, either way is fine).
The ["natural" order](https://pypi.org/project/natsort/#quick-description)
is used, so if numbers aren't zero-padded, it doesn't hurt. Also if the numbering
doesn't start at 1 or has a different number of digits, the script still works.

```
ROOT
  - King James Version
    - AT
      - 01_gen
        - ch01.mp3
        - ch02.mp3
        - ... (more chapters)
      - ... (more books)
    - NT
      - 01_mat
        - ch01.mp3
        - ch02.mp3
        - ... (more chapters)
      - ... (more books)
  - World English Bible
    - AT
      - 01_genesis.mp3
      - 02_exodus.mp3
      - ... (more books)
    - NT
      - 01_matthew.mp3
      - 02_mark.mp3
      - ... (more books)
  - ... (more bibles)
```

## Further possibilities

If you want to collect the MP3 files after adding the appropriate ID3 tags,
you can use the following shell command (put an `echo` before the `mv` to test it):

```
find . -name '*.mp3' | while read file; do \
  newfile=$(echo "$file" | sed -e 's#^\(./[^/]\+/[^/]\+/[^/]\+\)/\([^/]\+.mp3\)$#\1_\2#'); \
  mv -v "$file" "$newfile"; \
done
```