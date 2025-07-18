from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static

class ViewNoteScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"IP: {self.app.ip_address}", classes="title")
        yield Static("", id="note-info")
        yield Button("Вернуться", id="back")
        yield Footer()

    def on_mount(self) -> None:
        result = self.app.db.check_ip(self.app.ip_address)
        if result:
            note, created_at = result
            self.query_one("#note-info").update(f"Заметка: {note}\nСоздано: {created_at}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
