from rich.style import Style
from rich.theme import Theme

# Tema personalizado
CUSTOM_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green",
    "prompt": "cyan bold",
    "user": "blue",
    "assistant": "green"
})

# Estilos para painéis
PANEL_STYLES = {
    "user": Style(color="blue", bold=True),
    "assistant": Style(color="green"),
    "error": Style(color="red", bold=True),
    "info": Style(color="cyan")
}