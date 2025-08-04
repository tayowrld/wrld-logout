#!/usr/bin/env python3
import os
import subprocess
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


def ensure_css():
    """
    Ensure the theme directory and default CSS exist, then return the CSS path.
    """
    config_dir = os.path.join(os.path.expanduser('~'), '.config', 'wrld-logout')
    css_file = os.path.join(config_dir, 'style.css')
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    if not os.path.isfile(css_file):
        default_css = """
window {
  background-color: #FDF6E3;
  border-radius: 1px;
}
button {
  background-color: transparent;
  color: #323D43;
  border: none;
  font-weight:600;
  padding: 8px 16px;
  font-size: 16px;
}
button:hover {
  background-color: #E4E1CD;
}
"""
        with open(css_file, 'w') as f:
            f.write(default_css)
    return css_file


def load_css(css_path):
    """
    Load CSS from the given path into the GTK style context.
    """
    provider = Gtk.CssProvider()
    try:
        provider.load_from_path(css_path)
    except Exception as e:
        print(f"Failed to load CSS: {e}", file=sys.stderr)
        return
    screen = Gdk.Screen.get_default()
    Gtk.StyleContext.add_provider_for_screen(
        screen,
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def on_logout(widget):
    subprocess.run(['hyprctl', 'dispatch', 'exit'])
    Gtk.main_quit()


def on_shutdown(widget):
    subprocess.run(['systemctl', 'poweroff'])
    Gtk.main_quit()


def on_restart(widget):
    subprocess.run(['systemctl', 'reboot'])
    Gtk.main_quit()


def on_suspend(widget):
    subprocess.run(['systemctl', 'suspend'])
    Gtk.main_quit()

def on_cancel(widget):
    Gtk.main_quit()

def main():
    css_path = ensure_css()
    load_css(css_path)

    # Create main window
    win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    win.set_title("WrldLogout")
    try:
        win.set_wmclass("wrld-logout", "WrldLogout")
    except AttributeError:
        pass
    win.set_decorated(False)
    win.set_keep_above(True)
    win.set_type_hint(Gdk.WindowTypeHint.DIALOG)

    # Fix window size (min/max) and disable resize
    geom = Gdk.Geometry()
    geom.min_width = 200
    geom.min_height = 150
    geom.max_width = 400
    geom.max_height = 250
    win.set_geometry_hints(win, geom,
                           Gdk.WindowHints.MIN_SIZE | Gdk.WindowHints.MAX_SIZE)
    win.set_default_size(200, 150)
    win.set_resizable(False)

    # Center on screen
    win.set_position(Gtk.WindowPosition.CENTER)
    win.connect('destroy', Gtk.main_quit)

    # Container for buttons
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    box.set_margin_top(10)
    box.set_margin_bottom(10)
    box.set_margin_start(10)
    box.set_margin_end(10)
    win.add(box)

    # Button definitions
    actions = [
        ('Logout', on_logout),
        ('Shutdown', on_shutdown),
        ('Restart', on_restart),
        ('Suspend', on_suspend),
        ('Cancel', on_cancel),
    ]

    for label, callback in actions:
        btn = Gtk.Button(label=label)
        btn.set_relief(Gtk.ReliefStyle.NONE)
        btn.connect('clicked', callback)
        box.pack_start(btn, True, True, 0)

    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
