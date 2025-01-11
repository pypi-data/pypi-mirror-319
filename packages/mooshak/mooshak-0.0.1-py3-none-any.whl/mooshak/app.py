from textual.app import App

from mooshak.screens import HomeScreen  # TODO Cleanup imports


class Mooshak(App):
    """Coming Soon."""

    CSS_PATH = ["app.tcss"]

    SCREENS = {"home": HomeScreen}

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def on_mount(self) -> None:
        """Push home screen on mount."""
        self.push_screen("home")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
