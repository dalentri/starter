from pathlib import Path
from tinytag import TinyTag
import re


# Reads the user specified music directory
class ReadDir:
    # straight forward init
    def __init__(self) -> None:
        self.path = None
        self.unformatted_times = []

    # Scans the user's folder for files / directories
    def scan_folder(self):
        music_folder = Path.home() / "Music"
        self.path = music_folder
        # Inits a list of the music that will be found later
        music_list = []
        unformatted_times = []

        # Goes through the folder and lists all files
        for item in music_folder.iterdir():
            if (
                not item.name.endswith(".m4a")
                and not item.name.startswith(".")
                and item.is_file()
            ):
                tag: TinyTag = TinyTag.get(item)
                # Keep a copy of the unformatted times
                unformatted_times.append(tag.duration)

                mins, secs = divmod(round(tag.duration), 60)
                formatted_time = f"{mins:01}:{secs:02}"

                # Regex pattern to clean title and artist text
                CLEAN_PATTERN = re.compile(r"[^\w\s\-\(\)\.\[\]\u4e00-\u9fff]")

                song_data = (
                    CLEAN_PATTERN.sub("", tag.title)
                    if tag.title
                    else CLEAN_PATTERN.sub("", item.name),
                    CLEAN_PATTERN.sub("", tag.artist) if tag.artist else "Unknown",
                    formatted_time,
                    str(item),
                )

                # Append the tuple to the list
                music_list.append(song_data)

        self.unformatted_times = unformatted_times
        return music_list

    def get_full_path(self, filename: str):
        full_path = Path.home() / filename
        print(full_path)
        return str(full_path)
