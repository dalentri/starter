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

        # Goes through the folder and lists all files
        for item in music_folder.iterdir():
            print(item.name)
