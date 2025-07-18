from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input

class AddNoteScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"IP: {self.app.ip_address}", classes="title")
        yield Input(placeholder="Введите заметку для этого IP...")
        yield Button("Сохранить", id="save")
        yield Button("Отмена", id="cancel")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            note = self.query_one(Input).value
            if note:
                self.app.db.save_ip(self.app.ip_address, note)
                self.app.pop_screen()
        elif event.button.id == "cancel":
            self.app.pop_screen()
