"""GUI components and representation."""

# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Parker L

from nicegui import ui


def run_gui() -> None:
    """Render the table diff GUI."""
    # TODO: Implement the actual GUI mechanism.
    ui.icon("thumb_up")
    ui.markdown("This is **Markdown**.")
    ui.html("This is <strong>HTML</strong>.")
    with ui.row():
        ui.label("CSS").style("color: #888; font-weight: bold")
        ui.label("Tailwind").classes("font-serif")
        ui.label("Quasar").classes("q-ml-xl")
    ui.link("NiceGUI on GitHub", "https://github.com/zauberzeug/nicegui")

    ui.run()


run_gui()
