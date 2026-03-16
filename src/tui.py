from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.binding import Binding
from src.read_dir import ReadDir


class TUI(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="s", action="play_song", description="Play selected song song"),
        # vim bindings
        Binding(key="j", action="move_down", description="Move down"),
        Binding(key="k", action="move_up", description="Move up"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.read_dir = ReadDir()

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
