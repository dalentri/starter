# Import the files from the same directory
from . import find_path, read_dir, music_controls, tui
import time


def main():
    # Init find folder class
    find_folder = find_path.FindPath()

    platform, path = find_folder.find_platform()

    # Init scan directory class and pass in prev platform and path variables
    scan_directory = read_dir.ReadDir(platform, path)

    scan_directory.scan_folder()

    control_music = music_controls.MusicControls(
        scan_directory.get_full_path("KlassikBlendz.wav")
    )
    control_music.load_song()
    control_music.play_song()
    time.sleep(10)


if __name__ == "__main__":
    main()
