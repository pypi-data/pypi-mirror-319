from textual.app import RenderResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Footer, Static

LOGO_ASCII = """
                          _
                        (( )_,     ,
                 .--.    \\ '/     /.\\
                     )   / \\=    /O o\\     _
                    (   / _/    /' o O| ,_( ))___     (`
                     `-|   )_  /o_O_'_(  \\'    _ `\\    )
                       `\"\"\"\"`            =`---<___/---'
                                             "`

 ██████   ██████                           █████                █████
░░██████ ██████                           ░░███                ░░███
 ░███░█████░███   ██████   ██████   █████  ░███████    ██████   ░███ █████
 ░███░░███ ░███  ███░░███ ███░░███ ███░░   ░███░░███  ░░░░░███  ░███░░███
 ░███ ░░░  ░███ ░███ ░███░███ ░███░░█████  ░███ ░███   ███████  ░██████░
 ░███      ░███ ░███ ░███░███ ░███ ░░░░███ ░███ ░███  ███░░███  ░███░░███
 █████     █████░░██████ ░░██████  ██████  ████ █████░░████████ ████ █████
░░░░░     ░░░░░  ░░░░░░   ░░░░░░  ░░░░░░  ░░░░ ░░░░░  ░░░░░░░░ ░░░░ ░░░░░
"""


class MooshakLogo(Static):
    """Mooshak logo widget."""

    def render(self) -> RenderResult:
        """Render LOGO ASCII."""
        return LOGO_ASCII


class HomeScreen(Screen):
    """Home Screen."""

    def compose(self):
        """Compose."""
        with Center():
            yield MooshakLogo(id="logo")
        with Center():
            yield Static("Coming Soon!", classes="width-auto")
        yield Footer()
