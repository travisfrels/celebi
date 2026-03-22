import enum
from tkinter import ttk

try:
    import winreg
except ImportError:
    winreg = None

_REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
_REGISTRY_KEY = "AppsUseLightTheme"


class Theme(enum.Enum):
    LIGHT = "light"
    DARK = "dark"


def detect_system_theme():
    """Detect Windows light/dark mode from registry. Falls back to LIGHT."""
    if winreg is None:
        return Theme.LIGHT

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REGISTRY_PATH) as key:
            value, _ = winreg.QueryValueEx(key, _REGISTRY_KEY)
            return Theme.DARK if value == 0 else Theme.LIGHT
    except (OSError, FileNotFoundError):
        return Theme.LIGHT


_PALETTES = {
    Theme.LIGHT: {
        "bg": "#f0f0f0",
        "fg": "#1a1a1a",
        "field_bg": "#ffffff",
        "field_fg": "#1a1a1a",
        "select_bg": "#0078d4",
        "select_fg": "#ffffff",
        "button_bg": "#e1e1e1",
        "button_fg": "#1a1a1a",
        "heading_bg": "#d8d8d8",
        "heading_fg": "#1a1a1a",
        "border": "#a0a0a0",
        "trough": "#c8c8c8",
        "indicator": "#ffffff",
    },
    Theme.DARK: {
        "bg": "#2d2d2d",
        "fg": "#d4d4d4",
        "field_bg": "#1e1e1e",
        "field_fg": "#d4d4d4",
        "select_bg": "#264f78",
        "select_fg": "#ffffff",
        "button_bg": "#3c3c3c",
        "button_fg": "#d4d4d4",
        "heading_bg": "#3c3c3c",
        "heading_fg": "#d4d4d4",
        "border": "#555555",
        "trough": "#1e1e1e",
        "indicator": "#2d2d2d",
    },
}


def get_palette(theme):
    """Return the color palette dict for the given theme."""
    return dict(_PALETTES[theme])


def apply_theme(root, theme):
    """Configure ttk.Style and root window background for the given theme."""
    palette = _PALETTES[theme]
    style = ttk.Style(root)
    style.theme_use("clam")

    root.configure(bg=palette["bg"])

    style.configure("TFrame", background=palette["bg"])

    style.configure(
        "TLabelframe",
        background=palette["bg"],
        foreground=palette["fg"],
        bordercolor=palette["border"],
    )
    style.configure(
        "TLabelframe.Label",
        background=palette["bg"],
        foreground=palette["fg"],
    )

    style.configure(
        "TLabel",
        background=palette["bg"],
        foreground=palette["fg"],
    )

    style.configure(
        "TButton",
        background=palette["button_bg"],
        foreground=palette["button_fg"],
        bordercolor=palette["border"],
    )
    style.map(
        "TButton",
        background=[("active", palette["select_bg"])],
        foreground=[("active", palette["select_fg"])],
    )

    style.configure(
        "TSpinbox",
        fieldbackground=palette["field_bg"],
        foreground=palette["field_fg"],
        background=palette["button_bg"],
        bordercolor=palette["border"],
        arrowcolor=palette["fg"],
        selectbackground=palette["select_bg"],
        selectforeground=palette["select_fg"],
    )

    style.configure(
        "TRadiobutton",
        background=palette["bg"],
        foreground=palette["fg"],
        indicatorcolor=palette["indicator"],
        indicatorbackground=palette["indicator"],
    )
    style.map(
        "TRadiobutton",
        background=[("active", palette["bg"])],
        indicatorcolor=[("selected", palette["select_bg"])],
    )

    style.configure(
        "Treeview",
        background=palette["field_bg"],
        foreground=palette["field_fg"],
        fieldbackground=palette["field_bg"],
        selectbackground=palette["select_bg"],
        selectforeground=palette["select_fg"],
        bordercolor=palette["border"],
    )
    style.configure(
        "Treeview.Heading",
        background=palette["heading_bg"],
        foreground=palette["heading_fg"],
        bordercolor=palette["border"],
    )
    style.map(
        "Treeview.Heading",
        background=[("active", palette["select_bg"])],
        foreground=[("active", palette["select_fg"])],
    )

    style.configure(
        "TScrollbar",
        background=palette["button_bg"],
        troughcolor=palette["trough"],
        bordercolor=palette["border"],
        arrowcolor=palette["fg"],
    )
