import platform
from pathlib import Path


class FindPath:
    def __init__(self) -> None:
        self.user_path = None

    # Finds the user's platform
    def find_platform(self) -> tuple:

        user_platform = platform.system()
        user_path = Path.home() / "Music"

        print(f"Platform: {user_platform}")
        print(f"Path: {user_path}")
        # We return both the platform and the path to later pass into ReadDir
        # Macos
        if user_platform == "Darwin":
            return "Darwin", user_path
        # Win
        elif user_platform == "Windows":
            return "Windows", user_path
        # Linux
        elif user_platform == "Linux":
            return "Linux", user_path
        else:
            return "Platform not supported.", "Path not found."
