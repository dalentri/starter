from pathlib import Path


# Reads the user specified music directory
class ReadDir:
    # straight forward init
    def __init__(self, platform, path) -> None:
        self.platform = platform
        self.path = path

    # Scans the user's folder for files / directories
    def scan_folder(self):
        music_folder = Path(self.path)
        # Inits a list of the music that will be found later
        music_list = []

        # Goes through the folder and lists all files
        # TODO: Make this iterable in tui
        for item in music_folder.iterdir():
            if (
                not item.name.endswith(".m4a")
                and not item.name.startswith(".")
                and item.is_file()
            ):
                print(item.name)
                print(item)

                # Append the a tuple containing both the item name and the path to the item to the list
                music_list.append((item.name, str(item)))

    def get_full_path(self, filename: str):
        full_path = Path(self.path) / filename
        print(full_path)
        return str(full_path)
