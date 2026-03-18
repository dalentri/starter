from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.binding import Binding
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

    # Populates the tui with the defined components
    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "starter"
        table = self.query_one(DataTable)

        table.add_column("title")
        table.add_column("artist")
        table.add_column("duration")
        table.add_column("path")

        songs = self.read_dir.scan_folder()
        table.add_rows(songs)

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
        cur_pos = table.cursor_row
        song_row = table.get_row_at(cur_pos)

        song_path = song_row[3]

        # If music not playing, play song
        if not self.music_controls.song_playing:
            # If the song played, resume it
            if self.music_controls.song_elapsed:
                self.music_controls.unpause_song()
            # If the song hasn't played yet, start it
            else:
                self.music_controls.load_song(song_path)
                self.music_controls.play_song()
        # If music playing, pause the song
        else:
            self.music_controls.pause_song()
