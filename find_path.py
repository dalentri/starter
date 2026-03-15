import platform


class FindPath:
    # Finds the user's platform
    def find_platform(self) -> tuple[str, str]:
        user_platform = platform.system()
        print(f"Platform: {user_platform}")

        # We return both the platform and the path to later pass into ReadDir
        # Macos
        if user_platform == "Darwin":
            return "Darwin", "/Users/<User>/Music"
        # Win
        elif user_platform == "Windows":
            return "Windows", "C:\\Users\\<User>\\Music"
        # Linux
        elif user_platform == "Linux":
            return "Linux", "/home/<User>/Music"
        else:
            return "Platform not supported.", "Path not found."
