# Library imports
from textual.app import App, ComposeResult
from textual.widgets import DataTable, ProgressBar, Header, Footer, Label
from textual.containers import Center, Middle, Horizontal, Vertical
from textual.binding import Binding
from textual.content import Content
import re

# File imports
from src.read_dir import ReadDir
from src.music_controls import MusicControls


class TUI(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="h", action="play_pause", description="Play/pause"),
        # vim bindings
        Binding(key="j", action="move_down", description="Move down"),
        Binding(key="k", action="move_up", description="Move up"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.read_dir = ReadDir()
        self.music_controls = MusicControls()
        self.current_song = "No song currently playing."

    # Populates the tui with the defined components
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield DataTable()
            with Vertical():
                with Center():
                    with Middle():
                        yield Label(self.current_song)
                        yield ProgressBar()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "starter"

        # DataTable
        table = self.query_one(DataTable)

        table.add_column("title", width=50)
        table.add_column("artist", width=20)
        table.add_column("duration")

        songs = self.read_dir.scan_folder()

        # Regex pattern to clean title and artist text
        CLEAN_PATTERN = re.compile(r"[^\w\s\-\(\)\.\[\]\u4e00-\u9fff]")

        # Stores the cleaned songs in a list
        clean_songs = [
            # tuple pattern for cleaned songs
            (
                CLEAN_PATTERN.sub("", song[0]),
                CLEAN_PATTERN.sub("", song[1]),
                song[2],
                song[3],
            )
            # iterates through the list of uncleaned songs until completed
            for song in songs
        ]

        # iterates through the cleaned songs and populates each row of the data table
        for song in clean_songs:
            # transform the title into a textual container and extract the text
            song_title = Content(song[0]).plain

            # If the length of the title is too long, cut it and add ellipses
            if len(song_title) > 50:
                song_title = song_title[:47] + "..."

            # populate the table
            table.add_row(song_title, song[1], song[2], key=song[3])

    # All keybind functions mentioned in the footer
    # Movement keybinds
    def action_move_down(self):
        table = self.query_one(DataTable)
        # Get the current row postition of the cursor
        cur_pos = table.cursor_row

        # If the cursor is at the end, wrap around
        if cur_pos == table.row_count - 1:
            table.move_cursor(row=0)
        else:
            table.move_cursor(row=cur_pos + 1)

    def action_move_up(self):
        table = self.query_one(DataTable)
        cur_pos = table.cursor_row

        if cur_pos == 0:
            table_end = table.row_count - 1
            table.move_cursor(row=table_end)
        else:
            table.move_cursor(row=cur_pos - 1)

    def action_play_pause(self):
        table = self.query_one(DataTable)
        progress_bar = self.query_one(ProgressBar)
        cur_pos = table.cursor_row
        row_key = table.ordered_rows[cur_pos]

        song_path = row_key.key.value

        self.query_one(Label).update(str(table.get_row_at(cur_pos)[0]))

        if self.music_controls.song_playing:
            if (
                self.music_controls.song_elapsed
                and self.music_controls.song_path == song_path
            ):
                self.music_controls.pause_song()
            else:
                self.music_controls.load_song(song_path)
                self.music_controls.play_song()
        else:
            self.music_controls.unpause_song()
