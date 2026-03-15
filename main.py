import find_path, read_dir


def main():
    # Init find folder class
    find_folder = find_path.FindPath()

    platform, path = find_folder.find_platform()

    # Init scan directory class and pass in prev platform and path variables
    scan_directory = read_dir.ReadDir(platform, path)

    scan_directory.scan_folder()


if __name__ == "__main__":
    main()
