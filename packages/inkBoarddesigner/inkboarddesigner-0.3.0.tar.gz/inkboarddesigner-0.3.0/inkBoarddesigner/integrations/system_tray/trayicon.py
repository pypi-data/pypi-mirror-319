
from typing import TYPE_CHECKING
import threading
import asyncio

from PIL import Image
from pathlib import Path

import pystray

import inkBoard
from inkBoard.constants import INKBOARD_ICON
from inkBoard.helpers import QuitInkboard

from . import system_tray_entry

if TYPE_CHECKING:
    from inkBoard import core as CORE, config
    from inkBoarddesigner.platforms.desktop import device as desktop

_LOGGER = inkBoard.getLogger(__name__)

default_config = system_tray_entry(icon="circle", hide_window=True, toolwindow=False)

class HIDEACTIONS:
    ICONIFY = "iconify"
    WITHDRAW = "withdraw"

class TrayIcon(pystray.Icon):

    def __init__(self, core: "CORE", config: "config", **kwargs):
        self.__core = core
        tray_config = config["system_tray"]
        if not tray_config:
            tray_config = default_config
        else:
            tray_config = default_config.copy() | tray_config


        if tray_config.get("hide_window", False):
            if core.DESIGNER_RUN:
                _LOGGER.info("Not running system_tray with hide_window in the designer")
                self._minimise_action = HIDEACTIONS.ICONIFY
            else:
                self._minimise_action = HIDEACTIONS.WITHDRAW
        else:
            self._minimise_action = HIDEACTIONS.ICONIFY
        ##Other options to add: custom icon; custom name

        self._toolwindow = tray_config.get("toolwindow", False)

        if tray_config["icon"] == "circle":
            imgfile = Path(__file__).parent / "files" / f"icon_circle.ico"
        elif tray_config["icon"] == "droplet":
            imgfile = Path(__file__).parent / "files" / f"icon_droplet.ico"
        else:
            imgfile = Path(tray_config)
        img = Image.open(imgfile)

        menu = pystray.Menu(
            pystray.MenuItem(
                text="Minimise", action = self.minimise_window,
                default=True, visible=False
                ),
            pystray.MenuItem(
                text="Reload", action = self._reload_inkboard
            ),
            pystray.MenuItem(
                text="Quit", action = self._quit_inkboard
            ),
        )
        super().__init__("inkBoard", img, "inkBoard", menu, **kwargs)


    @property
    def _device(self) -> "desktop.Device":
        return self.__core.device

    @property
    def window(self):
        return self._device.window
    
    def minimise_window(self, item):
        "Minimise the dashboard window"
        self._device._call_in_main_thread(self._minimise_window, item)

    def _minimise_window(self, item):
        "Minimises the window. Must be called in the main thread"
        _LOGGER.debug(f"Minimising window via {item}")

        if self.window.wm_state() != "normal":
            if self._minimise_action == HIDEACTIONS.WITHDRAW:
                ##This simply makes the animation of the window appearing a lot smoother
                self.window.iconify()
            self.window.deiconify()
        else:
            if self._minimise_action == HIDEACTIONS.ICONIFY:
                self.window.withdraw()
            else:
                self.window.iconify()
        
        self.window.update()

    def _reload_inkboard(self, item):
        self.__core.screen.reload()
        self.stop()
    
    def _quit_inkboard(self, item):
        self.__core.screen.quit(QuitInkboard("Quit via systemtray"))
        self.stop()

    def start(self):
        if self._toolwindow:
            if self.__core.DESIGNER_RUN:
                _LOGGER.info("Hiding the designer from the taskbar is disabled")
            else:
                self.window.update_idletasks()
                self.window.wm_attributes("-toolwindow", True)
                
        self.run_detached()

