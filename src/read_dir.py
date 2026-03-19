from pathlib import Path
from tinytag import TinyTag
import re


# Reads the user specified music directory
class ReadDir:
    # straight forward init
    def __init__(self) -> None:
        self.path = None

    # Scans the user's folder for files / directories
    def scan_folder(self):
        music_folder = Path.home() / "Music"
        self.path = music_folder
        # Inits a list of the music that will be found later
        music_list = []
        CLEAN_PATTERN = re.compile(r"[^\w\s\-\(\)\.\[\]\u4e00-\u9fff]")

        # Goes through the folder and lists all files
        for item in music_folder.iterdir():
            if (
                not item.name.endswith(".m4a")
                and not item.name.startswith(".")
                and item.is_file()
            ):
                tag: TinyTag = TinyTag.get(item)

                song_data = (
                    tag.title or item.name,
                    tag.artist or "Unknown",
                    # TODO: Create a helper function that will format the duration
                    tag.duration,
                    str(item),
                )

                # Append the tuple to the list
                music_list.append(song_data)
        return music_list

    def get_full_path(self, filename: str):
        full_path = Path.home() / filename
        print(full_path)
        return str(full_path)
