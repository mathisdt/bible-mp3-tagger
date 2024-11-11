import os
import re
import sys

from mutagen.id3 import ID3, TIT2, TRCK, TALB, TPE1, Encoding
from mutagen.mp3 import MP3
from natsort import natsorted


def ls(path, criteria):
    result = list([f for f in os.scandir(path) if criteria(f)])
    return natsorted(result, key=lambda x: x.name)


at_books = [
    "1. Mose",
    "2. Mose",
    "3. Mose",
    "4. Mose",
    "5. Mose",
    "Josua",
    "Richter",
    "Rut",
    "1. Samuel",
    "2. Samuel",
    "1. Könige",
    "2. Könige",
    "1. Chronik",
    "2. Chronik",
    "Esra",
    "Nehemia",
    "Ester",
    "Hiob",
    "Psalmen",
    "Sprüche",
    "Prediger",
    "Hohelied",
    "Jesaja",
    "Jeremia",
    "Klagelieder",
    "Hesekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadja",
    "Jona",
    "Micha",
    "Nahum",
    "Habakuk",
    "Zefanja",
    "Haggai",
    "Sacharja",
    "Maleachi"
]
nt_books = [
    "Matthäus",
    "Markus",
    "Lukas",
    "Johannes",
    "Apostelgeschichte",
    "Römer",
    "1. Korinther",
    "2. Korinther",
    "Galater",
    "Epheser",
    "Philipper",
    "Kolosser",
    "1. Thessalonicher",
    "2. Thessalonicher",
    "1. Timotheus",
    "2. Timotheus",
    "Titus",
    "Philemon",
    "Hebräer",
    "Jakobus",
    "1. Petrus",
    "2. Petrus",
    "1. Johannes",
    "2. Johannes",
    "3. Johannes",
    "Judas",
    "Offenbarung"
]


def bookname(bible_part_name, index, singular=False):
    if bible_part_name == "AT":
        result = at_books[index]
        if result == "Psalmen" and singular:
            return "Psalm"
        else:
            return result
    else:
        return nt_books[index]


if len(sys.argv) < 2:
    print("you need to supply your MP3 bibles directory as first parameter")
    exit(1)

bibles = ls(sys.argv[1], lambda x: x.is_dir())

for bible in bibles:
    bible_name = bible.name
    print(f"\n{bible_name}")
    bible_parts = ls(bible, lambda x: x.is_dir())
    for bible_part in bible_parts:
        bible_part_name = bible_part.name
        print(f"  {bible_part_name}")
        book_dirs = ls(bible_part, lambda x: x.is_dir())
        book_index = 0
        track_number = 1
        if not book_dirs:
            # books are MP3 files
            book_files = ls(bible_part, lambda x: x.is_file() and re.match(r'^.+\.mp3$', x.name, re.IGNORECASE))
            for book_file in book_files:
                print(f"    FILE(BOOK): {book_file.name}")
                print(
                    f"      #{track_number}: Bibel - {bible_name} - {bible_part_name} - {bookname(bible_part_name, book_index)}")
                mp3 = MP3(book_file)
                mp3.delete()
                id3 = ID3()
                id3.add(TPE1(text=f"Bibel - {bible_name}", encoding=Encoding.UTF8))
                id3.add(TALB(text=f"Bibel - {bible_name} - {bible_part_name}", encoding=Encoding.UTF8))
                id3.add(TIT2(text=f"{bookname(bible_part_name, book_index)}", encoding=Encoding.UTF8))
                id3.add(TRCK(text=f"{track_number}", encoding=Encoding.UTF8))
                mp3.tags = id3
                mp3.save()
                book_index += 1
                track_number += 1
        else:
            # books are directories
            for book_dir in book_dirs:
                print(f"    DIR: {book_dir.name}")
                chapter_files = ls(book_dir, lambda x: x.is_file() and re.match(r'^.+\.mp3$', x.name, re.IGNORECASE))
                chapter_number = 1
                for chapter_file in chapter_files:
                    print(f"      FILE(CHAPTER): {chapter_file.name}")
                    print(
                        f"        #{track_number}: Bibel - {bible_name} - {bible_part_name} - {bookname(bible_part_name, book_index, True)} {chapter_number}")
                    mp3 = MP3(chapter_file)
                    mp3.delete()
                    id3 = ID3()
                    id3.add(TPE1(text=f"Bibel - {bible_name}", encoding=Encoding.UTF8))
                    id3.add(TALB(text=f"Bibel - {bible_name} - {bible_part_name}", encoding=Encoding.UTF8))
                    id3.add(TIT2(text=f"{bookname(bible_part_name, book_index, True)} {chapter_number}",
                                 encoding=Encoding.UTF8))
                    id3.add(TRCK(text=f"{track_number}", encoding=Encoding.UTF8))
                    mp3.tags = id3
                    mp3.save()
                    chapter_number += 1
                    track_number += 1
                book_index += 1
