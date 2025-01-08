from pathlib import Path

import marimo as mo

from blackfish import ORCA
from blackfish.mo import soc_absorption_spectrum_ui as ui

__generated_with = "marimo"

# File selector UI element
file_selector = mo.ui.file(label="Select ORCA output file")

# Initialize app state
mo.md("# SOC Absorption Spectrum Viewer")
mo.md("Select an ORCA output file to begin.")


# Get the file path either from UI or command line
def get_file_path():
    """Get file path from UI or command line args"""
    import sys

    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return file_selector.value


def update_plot():
    """Update the plot based on current UI state and file"""
    file_path = get_file_path()
    if not file_path:
        return mo.md("Please select a file")

    try:
        orca = ORCA(file_path)
        chart = orca.soc_absorption_spectrum_chart(
            fwhm=ui["fwhm"].value,
            peaks=ui["show"].value,
            peak_threshold=ui["threshold"].value,
        )
        return mo.vega(chart)
    except Exception as e:
        return mo.md(f"Error loading file: {str(e)}")


# Create layout
mo.hstack(
    [
        mo.vstack(
            [
                file_selector,
                ui["fwhm"],
                ui["threshold"],
                ui["show"],
            ],
            spacing=2,
        ),
        update_plot(),
    ],
    sizes=[1, 4],
)

# Update plot when UI changes
file_selector.on_change(lambda _: _)
ui["fwhm"].on_change(lambda _: _)
ui["threshold"].on_change(lambda _: _)
ui["show"].on_change(lambda _: _)
