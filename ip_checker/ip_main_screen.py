import aiohttp
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, LoadingIndicator
from textual.containers import Center, Vertical, Horizontal
from .add_note_screen import AddNoteScreen
from .view_note_screen import ViewNoteScreen
import ipaddress
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPMainScreen(Screen):
    CSS = """
    #ip-label {
        text-align: center;
        margin: 1 0;
        color: $accent;
        text-style: bold;
        border: green;
    }
    
    #status {
        text-align: center;
        margin: 1 0 2 0;
        min-height: 3;
        color: $text;
    }
    
    .buttons-container {
        align: center middle;
        width: auto;
        height: auto;
        margin: 1 0;
    }
    
    Button {
        width: 24;
        margin: 0 1 1 0;
    }
    
    Button.primary {
        background: $primary;
        color: auto;
    }
    
    Button.success {
        background: $success;
        color: auto;
    }
    
    Button.secondary {
        background: $secondary;
        color: auto;
    }
    
    .hidden {
        display: none;
    }
    
    .loading-container {
        align: center middle;
        height: 3;
    }
    
    .timestamp {
        text-align: center;
        margin-top: 1;
        color: $text-muted;
    }
    """

    def compose(self) -> ComposeResult:
        """Определяет структуру экрана."""
        yield Header()
        yield Center(
            Label("Определение вашего IP-адреса...", id="ip-label")
        )
        yield Center(
            Label("", id="status")
        )
        with Center(classes="loading-container"):
            yield LoadingIndicator(id="loading")
        
        with Center():
            with Vertical(classes="buttons-container"):
                yield Button("💾 Сохранить с заметкой", 
                            id="save-note", 
                            classes="primary hidden")
                yield Button("📝 Просмотреть заметку", 
                            id="view-note", 
                            classes="success hidden")
                yield Button("🔄 Обновить IP", 
                            id="refresh", 
                            classes="secondary")
        
        yield Footer()

    async def on_mount(self) -> None:
        """Вызывается при монтировании экрана."""
        await self.fetch_and_check_ip()

    async def fetch_and_check_ip(self):
        """Получает IP-адрес и проверяет его в базе данных."""
        ip_label = self.query_one("#ip-label")
        status = self.query_one("#status")
        save_button = self.query_one("#save-note")
        view_button = self.query_one("#view-note")
        loading = self.query_one("#loading")

        try:
            # Показать индикатор загрузки
            ip_label.update("⌛ Получаем ваш IP-адрес...")
            status.update("")
            loading.display = True

            # Выполняем запрос с таймаутом
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.ipify.org", timeout=5) as response:
                    response.raise_for_status()
                    ip = await response.text()

            # Валидация IP-адреса
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                raise ValueError("Некорректный IP-адрес")

            ip_label.update(f"IP: [bold]{ip}[/]")
            self.app.ip_address = ip

            # Проверка IP в базе данных
            result = self.app.db.check_ip(ip)
            if result:
                note, created_at = result
                status.update(f"✅ Этот IP уже сохранен в базе\n[dim]Заметка: {note}[/]\n[dim]Дата сохранения: {created_at}[/]")
                save_button.add_class("hidden")
                view_button.remove_class("hidden")
            else:
                status.update("‼️ Этот IP не найден в базе")
                save_button.remove_class("hidden")
                view_button.add_class("hidden")
        except aiohttp.ClientError as e:
            status.update(f"⚠️ [bold]Сетевая ошибка:[/] {str(e)}")
            logger.error(f"Сетевая ошибка при получении IP: {str(e)}")
        except ValueError as e:
            status.update(f"⚠️ [bold]Ошибка валидации:[/] {str(e)}")
            logger.error(f"Ошибка валидации IP: {str(e)}")
        except Exception as e:
            status.update(f"⛔ [bold]Неизвестная ошибка:[/] {str(e)}")
            logger.error(f"Неизвестная ошибка: {str(e)}")
        finally:
            # Скрыть индикатор загрузки
            loading.display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обрабатывает нажатия кнопок."""
        if event.button.id == "save-note":
            self.app.push_screen(AddNoteScreen())
        elif event.button.id == "view-note":
            self.app.push_screen(ViewNoteScreen())
        elif event.button.id == "refresh":
            self.app.call_later(self.fetch_and_check_ip)
