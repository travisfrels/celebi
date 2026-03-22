import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import MagicMock, patch

from src.theme import Theme, apply_theme, detect_system_theme, get_palette

_root = None


def setUpModule():
    global _root
    _root = tk.Tk()
    _root.withdraw()


def tearDownModule():
    global _root
    _root.destroy()
    _root = None


class TestThemeEnum(unittest.TestCase):
    def test_light_value(self):
        self.assertEqual(Theme.LIGHT.value, "light")

    def test_dark_value(self):
        self.assertEqual(Theme.DARK.value, "dark")

    def test_members(self):
        self.assertEqual(set(Theme), {Theme.LIGHT, Theme.DARK})


class TestDetectSystemTheme(unittest.TestCase):
    @patch("src.theme.winreg")
    def test_detects_dark_when_registry_returns_0(self, mock_winreg):
        mock_key = MagicMock()
        mock_winreg.OpenKey.return_value.__enter__ = MagicMock(return_value=mock_key)
        mock_winreg.OpenKey.return_value.__exit__ = MagicMock(return_value=False)
        mock_winreg.QueryValueEx.return_value = (0, 1)
        mock_winreg.HKEY_CURRENT_USER = 0x80000001

        self.assertEqual(detect_system_theme(), Theme.DARK)

    @patch("src.theme.winreg")
    def test_detects_light_when_registry_returns_1(self, mock_winreg):
        mock_key = MagicMock()
        mock_winreg.OpenKey.return_value.__enter__ = MagicMock(return_value=mock_key)
        mock_winreg.OpenKey.return_value.__exit__ = MagicMock(return_value=False)
        mock_winreg.QueryValueEx.return_value = (1, 1)
        mock_winreg.HKEY_CURRENT_USER = 0x80000001

        self.assertEqual(detect_system_theme(), Theme.LIGHT)

    @patch("src.theme.winreg")
    def test_falls_back_to_light_on_os_error(self, mock_winreg):
        mock_winreg.OpenKey.side_effect = OSError("Registry not found")
        mock_winreg.HKEY_CURRENT_USER = 0x80000001

        self.assertEqual(detect_system_theme(), Theme.LIGHT)

    @patch("src.theme.winreg")
    def test_falls_back_to_light_on_file_not_found(self, mock_winreg):
        mock_winreg.OpenKey.side_effect = FileNotFoundError("Key not found")
        mock_winreg.HKEY_CURRENT_USER = 0x80000001

        self.assertEqual(detect_system_theme(), Theme.LIGHT)

    @patch("src.theme.winreg", None)
    def test_falls_back_to_light_when_winreg_unavailable(self):
        self.assertEqual(detect_system_theme(), Theme.LIGHT)


class TestGetPalette(unittest.TestCase):
    def test_returns_dict(self):
        palette = get_palette(Theme.LIGHT)
        self.assertIsInstance(palette, dict)

    def test_contains_expected_keys(self):
        expected_keys = {
            "bg", "fg", "field_bg", "field_fg", "select_bg", "select_fg",
            "button_bg", "button_fg", "heading_bg", "heading_fg", "border",
            "trough", "indicator",
        }
        for theme in Theme:
            with self.subTest(theme=theme):
                palette = get_palette(theme)
                self.assertEqual(set(palette.keys()), expected_keys)

    def test_light_and_dark_differ(self):
        light = get_palette(Theme.LIGHT)
        dark = get_palette(Theme.DARK)
        self.assertNotEqual(light["bg"], dark["bg"])

    def test_returns_copy(self):
        palette = get_palette(Theme.LIGHT)
        palette["bg"] = "modified"
        fresh = get_palette(Theme.LIGHT)
        self.assertNotEqual(fresh["bg"], "modified")


class TestApplyTheme(unittest.TestCase):
    def setUp(self):
        self.root = _root
        self.style = None

    def tearDown(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()

    def _apply(self, theme):
        apply_theme(self.root, theme)
        self.style = ttk.Style(self.root)

    def test_light_sets_frame_background(self):
        self._apply(Theme.LIGHT)
        bg = self.style.lookup("TFrame", "background")
        self.assertTrue(bg, "TFrame background should be set")

    def test_dark_sets_frame_background(self):
        self._apply(Theme.DARK)
        bg = self.style.lookup("TFrame", "background")
        self.assertTrue(bg, "TFrame background should be set")

    def test_root_background_matches_palette(self):
        self._apply(Theme.DARK)
        root_bg = self.root.cget("bg")
        frame_bg = self.style.lookup("TFrame", "background")
        self.assertEqual(root_bg, frame_bg)

    def test_all_widget_types_configured(self):
        self._apply(Theme.DARK)
        widget_types = [
            "TFrame",
            "TLabel",
            "TButton",
            "TSpinbox",
            "TRadiobutton",
            "Treeview",
            "Treeview.Heading",
            "TScrollbar",
            "TLabelframe",
            "TLabelframe.Label",
        ]
        for widget_type in widget_types:
            with self.subTest(widget_type=widget_type):
                bg = self.style.lookup(widget_type, "background")
                self.assertTrue(bg, f"{widget_type} background should be set")

    def test_dark_and_light_produce_different_colors(self):
        apply_theme(self.root, Theme.LIGHT)
        style = ttk.Style(self.root)
        light_bg = style.lookup("TFrame", "background")

        apply_theme(self.root, Theme.DARK)
        dark_bg = style.lookup("TFrame", "background")

        self.assertNotEqual(light_bg, dark_bg)

    def test_treeview_heading_configured(self):
        self._apply(Theme.DARK)
        bg = self.style.lookup("Treeview.Heading", "background")
        fg = self.style.lookup("Treeview.Heading", "foreground")
        self.assertTrue(bg, "Treeview.Heading background should be set")
        self.assertTrue(fg, "Treeview.Heading foreground should be set")


class TestThemeIntegration(unittest.TestCase):
    def setUp(self):
        self.root = _root
        self.app = None

    def tearDown(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()

    def test_app_has_theme_applied(self):
        from src.app import CelebiApp

        self.app = CelebiApp(root=self.root)
        self.root.update()
        style = ttk.Style(self.root)
        bg = style.lookup("TFrame", "background")
        self.assertTrue(bg, "Theme should be applied when CelebiApp is created")

    def test_root_background_set_on_app_creation(self):
        from src.app import CelebiApp

        self.app = CelebiApp(root=self.root)
        self.root.update()
        root_bg = self.root.cget("bg")
        style = ttk.Style(self.root)
        frame_bg = style.lookup("TFrame", "background")
        self.assertEqual(root_bg, frame_bg)


if __name__ == "__main__":
    unittest.main()
