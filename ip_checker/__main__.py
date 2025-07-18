from textual.app import App
from .ip_main_screen import IPMainScreen
from .database import Database

class IPChecker(App):
    CSS = """
    .title {
        text-align: center;
        padding: 1;
        color: white;
        background: blue;
    }
    .hidden {
        display: none;
    }
    Label, Static {
        padding: 1;
    }
    Button {
        margin: 1;
    }
    ItemGrid {
        padding: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.ip_address = ""

    def on_mount(self) -> None:
        self.push_screen(IPMainScreen())

if __name__ == "__main__":
    IPChecker().run()
