from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.binding import Binding
from src.read_dir import ReadDir


class TUI(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="s", action="start", description="Start song"),
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
