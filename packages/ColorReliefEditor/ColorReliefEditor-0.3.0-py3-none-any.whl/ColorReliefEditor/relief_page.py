#  Copyright (c) 2024.
#   Copyright (c) 2024. Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the “Software”), to deal in the
#   Software without restriction,
#   including without limitation the rights to use, copy, modify, merge, publish, distribute,
#   sublicense, and/or sell copies
#   of the Software, and to permit persons to whom the Software is furnished to do so, subject to
#   the following conditions:
#  #
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#  #
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE
#   WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
#   EVENT SHALL THE AUTHORS OR
#   COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#   CONTRACT, TORT OR
#   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#  #
#   This uses QT for some components which has the primary open-source license is the GNU Lesser
#   General Public License v. 3 (“LGPL”).
#   With the LGPL license option, you can use the essential libraries and some add-on libraries
#   of Qt.
#   See https://www.qt.io/licensing/open-source-lgpl-obligations for QT details.
from PyQt6.QtWidgets import QVBoxLayout
from YMLEditor.settings_widget import SettingsWidget

from ColorReliefEditor.instructions import get_instructions
from ColorReliefEditor.preview_widget import PreviewWidget
from ColorReliefEditor.tab_page import TabPage, expanding_vertical_spacer


class ReliefPage(TabPage):
    """
    A widget for running Makefile commands to generate a Color Relief TIFF image.

    **Methods**:
    """

    def __init__(self, main, name):
        """
        Initialize

        Args:
            main (MainClass): Reference to the main application class.
            name (str): Name of the page.
        """
        # Set up display format for settings in basic mode and expert mode

        # Make layer label large
        label_style = f"font-size: {main.font_size + 5}px; "

        formats = {
            "expert": {
                "NAMES.@LAYER": ("", "read_only", None, 180, label_style),
                "MERGE_CALC": ("Calc ", "text_edit", r"^--calc=[^ ]*(?=.*A)(?=.*B)[^ ]*$", 280),
                "PUBLISH": ("Publish To", "text_edit", None, 280),
                "QUIET": ("Quiet Mode", "combo", ["-q", "-v", "--version"], 100),
            }, "basic": {
            },
        }

        # Get basic or expert mode
        mode = main.app_config["MODE"]

        # Widget for editing config settings
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(0, 0, 0, 0)  # No external margins
        settings_layout.setSpacing(5)  # Internal padding between widgets

        self.settings_widget = SettingsWidget(
            main.proj_config, formats, mode, verbose=main.verbose, text_edit_height=60,
            error_style="color: crimson;"
        )
        settings_layout.addWidget(self.settings_widget)
        settings_layout.addItem(expanding_vertical_spacer(10))

        super().__init__(
            main, name, on_exit_callback=main.proj_config.save, on_enter_callback=self.display
        )

        # Widget for building and managing images
        if mode == "expert":
            button_flags = ["make", "view", "publish", "cancel", "clean"]
        else:
            button_flags = ["make", "view"]
        self.preview = PreviewWidget(
            main, self.tab_name, self.settings_widget, False, main.proj_config.save, button_flags
        )

        widgets = [settings_layout, self.preview]
        stretch = [1, 8]

        # Instructions
        if self.main.app_config["INSTRUCTIONS"] == "show":
            instructions = get_instructions(self.tab_name, (mode == "basic"))
        else:
            instructions = None

        self.create_page(
            widgets, None, instructions, self.tab_name, vertical=False, stretch=stretch
        )

    def display(self):
        self.settings_widget.display()
        if self.preview:
            self.preview.display()
