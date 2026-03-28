# Library imports
import pygame
from textual.app import App, ComposeResult
from textual.widgets import DataTable, ProgressBar, Header, Footer, Label
from textual.containers import Center, Middle, Horizontal, Vertical
from textual.binding import Binding
from textual.content import Content

# File imports
from src.read_dir import ReadDir
from src.music_controls import MusicControls


class TUI(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="h", action="play_pause", description="Play/pause"),
        Binding(key="r", action="repeat_song", description="Repeat"),
        # vim bindings
        Binding(key="j", action="move_down", description="Move down"),
        Binding(key="k", action="move_up", description="Move up"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.read_dir = ReadDir()
        self.music_controls = MusicControls()
        self.current_song = "No song currently playing."
        self.song_index = 0
        self.song_duration = 0

    # Populates the tui with the defined components
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield DataTable()
            with Vertical(id="right-side"):
                with Middle():
                    with Center():
                        with Horizontal(id="status-row"):
                            yield Label(self.current_song)
                            yield Label("", id="repeat-label")
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

        # iterates through the cleaned songs and populates each row of the data table
        for song in songs:
            # transform the title into a textual container and extract the text
            song_title = Content(song[0]).plain

            # If the length of the title is too long, cut it and add ellipses
            if len(song_title) > 50:
                song_title = song_title[:47] + "..."

            # populate the table
            table.add_row(song_title, song[1], song[2], key=song[3])

        self.track_timer = self.set_interval(1, self.update_song_progress, pause=True)
        self.set_interval(0.1, self.check_pygame_events)

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
        self.song_index = cur_pos
        row_key = table.ordered_rows[cur_pos]

        song_path = row_key.key.value

        self.query_one(Label).update(str(table.get_row_at(cur_pos)[0]))
        # set the current song duration from the array in the read_dir class
        self.song_duration = self.read_dir.unformatted_times[self.song_index]

        if self.music_controls.song_playing:
            if (
                self.music_controls.song_elapsed
                and self.music_controls.song_path == song_path
            ):
                self.music_controls.pause_song()
                self.track_timer.pause()
            else:
                self.music_controls.load_song(song_path)
                self.music_controls.play_song()
                self.repeat_mode = False
                self.track_timer.resume()
        else:
            self.music_controls.unpause_song()
            self.track_timer.resume()

    def action_repeat_song(self):
        self.music_controls.repeat_mode = not self.music_controls.repeat_mode
        label_text = "↻" if self.music_controls.repeat_mode else ""

        self.query_one("#repeat-label", Label).update(label_text)

    def check_pygame_events(self):
        for event in pygame.event.get():
            if (
                event.type == self.music_controls.SONG_FINISHED
                and self.music_controls.repeat_mode
            ):
                self.music_controls.play_song()

    def update_song_progress(self):
        # Gets the current time of the currently playing song
        current_time = self.music_controls.get_pos() / 1000
        total_time = self.song_duration
        # Updates the progress bar to reflect the current song's time
        self.query_one(ProgressBar).update(total=total_time, progress=current_time)
