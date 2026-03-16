from textual.app import App, ComposeResult
from textual.widgets import DataTable
from src.read_dir import ReadDir


class TUI(App):
    CSS_PATH = "tui.tcss"

    def __init__(self) -> None:
        super().__init__()
        self.read_dir = ReadDir()

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        # FIX: bro this aint working bruh omg *like heaby sigh emoji*
        table = self.query_one(DataTable)

        table.add_column("title")
        table.add_column("artist")
        table.add_column("duration")
        table.add_column("path")

        songs = self.read_dir.scan_folder()
        table.add_rows(songs)
