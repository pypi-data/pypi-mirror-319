from dataclasses import dataclass
import re
import time
import typing
from pygetwindow import Win32Window
import screeninfo
from pywinlayout import utils

@dataclass
class Settings:
    """Configuration settings for window layout management.
    
    Attributes:
        monitor_margins_x (int): Horizontal margin from monitor edges in pixels
        monitor_margins_y (int): Vertical margin from monitor edges in pixels
        elapsed_time (int): Time delay in milliseconds (note: typo in original)
        min_wnd_width (int): Minimum window width in pixels
        min_wnd_height (int): Minimum window height in pixels
        max_wnd_width (int): Maximum window width in pixels (-1 for no limit)
        max_wnd_height (int): Maximum window height in pixels (-1 for no limit)
    """
    monitor_margins_x : int = 5
    monitor_margins_y : int = 5
    elaspsed_time : int = 1000
    min_wnd_width : int = 100
    min_wnd_height : int = 100
    max_wnd_width : int = -1
    max_wnd_height : int = -1
    
class PyWinLayout:
    @classmethod
    def matchWnds(cls, matches: typing.List[str] = []) -> 'PyWinLayout':
        wnds = []
        for wnd in utils.get_all_visible_windows():
            wnd : Win32Window
            if matches and any(re.match(re.escape(m).replace('\\*', '.*'), wnd.title) for m in matches):
                wnds.append(wnd)
        return cls(wnds)
    
    @classmethod
    def matchProcs(cls, matches: typing.List[str] = []) -> 'PyWinLayout':
        import psutil
        wnds = []
        for wnd in utils.get_all_visible_windows():
            wnd : Win32Window
            try:
                pid = utils.get_pid_from_hwnd(wnd._hWnd)
                proc = psutil.Process(pid)
                for m in matches:
                    escaped = re.escape(m).replace('\\*', '.*')
                    if re.match(escaped, proc.name()):
                        wnds.append(wnd)
                        break
                    elif re.match(escaped, proc.exe()):
                        wnds.append(wnd)
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return cls(wnds)

    @classmethod
    def allWindows(cls) -> 'PyWinLayout':
        return cls(utils.get_all_visible_windows())

    @classmethod
    def allWindowsOnMonitor(cls, *monitors : screeninfo.Monitor | int) -> 'PyWinLayout':
        """Get all windows that are primarily on the specified monitor(s).
        
        Args:
            *monitors: Monitor objects or indices to check. If none provided, uses primary monitor.
            
        Returns:
            PyWinLayout: New instance containing windows on the specified monitor(s)
        """
        # Get monitor dimensions
        monitor_areas = []
        for mon in monitors:
            monitor_areas.append(utils.get_monitor_dimensions(mon))
            
        if not monitor_areas:
            # Default to primary monitor if none specified
            monitors = [next(m for m in screeninfo.get_monitors() if m.is_primary)]
            monitor_areas = [utils.get_monitor_dimensions(monitors[0])]
            
        # Find windows primarily on these monitors
        wnds = []
        for wnd in utils.get_all_visible_windows():
            # Check if window center is in any monitor area
            for monitor_dims in monitor_areas:
                if utils.is_window_on_monitor(wnd, monitor_dims):
                    wnds.append(wnd)
                    break
                    
        return cls(wnds)

    def __init__(self, wnds :typing.List[Win32Window], settings : Settings = Settings()):
        self.__wnds = wnds
        self.__settings = settings
        
    @property
    def wnds(self):
        return self.__wnds
    
    @property
    def settings(self):
        return self.__settings

    def simpleGrid(self, string: str, monitor: typing.Union[screeninfo.Monitor, int, None] = None) -> None:
        # Parse grid dimensions from string (format: rowXcol)
        try:
            row, col = map(int, string.lower().split('x'))
        except (ValueError, AttributeError):
            raise ValueError("Invalid grid format. Expected 'rowXcol' (e.g. '2x3')")

        if row <= 0 or col <= 0:
            raise ValueError("Grid dimensions must be positive integers")
        
        if not self.wnds:
            raise ValueError("No windows to arrange")

        # Get monitor dimensions
        mon_width, mon_height, mon_x, mon_y = utils.get_monitor_dimensions(monitor)

        # Calculate window dimensions
        window_width = mon_width // col
        window_height = mon_height // row

        # Apply settings constraints
        window_width, window_height = utils.apply_window_constraints(window_width, window_height, self.settings)

        # Apply margins
        mon_x += self.settings.monitor_margins_x
        mon_y += self.settings.monitor_margins_y
        mon_width -= 2 * self.settings.monitor_margins_x
        mon_height -= 2 * self.settings.monitor_margins_y

        # Arrange windows
        for index, window in enumerate(self.wnds):
            if index >= row * col:
                break

            new_x = (index % col) * window_width + mon_x
            new_y = (index // col) * window_height + mon_y

            utils.activate_wnd(window)
            if window.isMaximized:
                window.restore()
            window.resizeTo(window_width, window_height)
            window.moveTo(new_x, new_y)
            time.sleep(self.settings.elaspsed_time / 1000)


    def middleStack(self, monitor=None, offset=20, direction="right"):
        """
        Arrange windows in a middle stack layout, with the first window centered
        and subsequent windows stacked behind with slight offset.

        Args:
            monitor (int or screeninfo.Monitor, optional): Monitor to use for arrangement.
                If int, specifies the monitor index. If None, uses primary monitor.
            offset (int, optional): Pixels to offset each stacked window. Defaults to 20.
            direction (str, optional): Direction to stack windows ("right", "left", "up", "down").
                Defaults to "right".
        """
        # Get monitor dimensions
        mon_width, mon_height, mon_x, mon_y = utils.get_monitor_dimensions(monitor)

        # Apply margins
        mon_x += self.settings.monitor_margins_x
        mon_y += self.settings.monitor_margins_y
        mon_width -= 2 * self.settings.monitor_margins_x
        mon_height -= 2 * self.settings.monitor_margins_y

        # Calculate window dimensions
        window_width = mon_width // 2
        window_height = mon_height // 2

        # Apply settings constraints
        window_width, window_height = utils.apply_window_constraints(window_width, window_height, self.settings)

        # Calculate center position
        center_x = mon_x + (mon_width - window_width) // 2
        center_y = mon_y + (mon_height - window_height) // 2

        # Arrange windows
        for i, window in enumerate(self.wnds):
            utils.activate_wnd(window)
            if window.isMaximized:
                window.restore()
            window.resizeTo(window_width, window_height)
            
            if i == 0:
                # Center first window
                window.moveTo(center_x, center_y)
            else:
                # Stack subsequent windows with offset based on direction
                if direction.lower() == "right":
                    offset_x = center_x + (i * offset)
                    offset_y = center_y
                elif direction.lower() == "left":
                    offset_x = center_x - (i * offset)
                    offset_y = center_y
                elif direction.lower() == "down":
                    offset_x = center_x
                    offset_y = center_y + (i * offset)
                elif direction.lower() == "up":
                    offset_x = center_x
                    offset_y = center_y - (i * offset)
                else:
                    raise ValueError("Direction must be 'right', 'left', 'up', or 'down'")
                window.moveTo(offset_x, offset_y)
            
            time.sleep(self.settings.elaspsed_time / 1000)

    def grid(self, layout: str, monitors: typing.List[screeninfo.Monitor] = None) -> None:
        """Arrange windows in a grid pattern across multiple monitors.
        
        Args:
            layout (str): Grid layout in format "rows x columns" (e.g. "2x3")
            monitors (List[screeninfo.Monitor], optional): List of monitors to use. 
                If None, uses primary monitor first then others. Defaults to None.
        """
        if not self.wnds:
            return
            
        # Parse layout string
        try:
            rows, cols = map(int, layout.lower().split('x'))
            if rows <= 0 or cols <= 0:
                raise ValueError
        except: # noqa
            raise ValueError("Layout must be in format 'rows x columns' (e.g. '2x3')")

        # Get monitors if not provided
        if monitors is None:
            monitors = screeninfo.get_monitors()
            # Sort so primary is first
            monitors.sort(key=lambda m: not m.is_primary)

        cells_per_monitor = rows * cols
        total_windows = len(self.wnds)
        
        for monitor_idx, monitor in enumerate(monitors):
            # Calculate windows for this monitor
            start_idx = monitor_idx * cells_per_monitor
            end_idx = min(start_idx + cells_per_monitor, total_windows)
            if start_idx >= total_windows:
                break
                
            monitor_windows = self.wnds[start_idx:end_idx]
            
            # Calculate monitor work area
            mon_x = monitor.x + self.settings.monitor_margins_x
            mon_y = monitor.y + self.settings.monitor_margins_y 
            mon_width = monitor.width - (2 * self.settings.monitor_margins_x)
            mon_height = monitor.height - (2 * self.settings.monitor_margins_y)

            # Calculate cell dimensions
            cell_width = mon_width // cols
            cell_height = mon_height // rows
            
            # Apply size constraints
            cell_width, cell_height = utils.apply_window_constraints(cell_width, cell_height, self.settings)

            # Position windows in grid
            for i, window in enumerate(monitor_windows):
                row = i // cols
                col = i % cols
                
                utils.activate_wnd(window)
                if window.isMaximized:
                    window.restore()
                    
                x = mon_x + (col * cell_width)
                y = mon_y + (row * cell_height)
                
                window.resizeTo(cell_width, cell_height)
                window.moveTo(x, y)
                
                time.sleep(self.settings.elaspsed_time / 1000)

    def moodboard(self, layouts : typing.List[typing.Dict[str, typing.Any]] = None, matchTo : dict = None, randomAll : bool = False, monitor : typing.List[screeninfo.Monitor] = None):
        """Position windows according to custom layout specifications, ensuring no overlap.
        
        Args:
            layouts (list[dict], optional): List of layout specifications for each window.
                Each dict can contain:
                - minheight (int, optional): Minimum height for the window
                - maxheight (int, optional): Maximum height for the window  
                - minwidth (int, optional): Minimum width for the window
                - maxwidth (int, optional): Maximum width for the window
                - preferredMonitorList (list[int], optional): List of preferred monitor indices
                - random (bool, optional): Whether to randomize the window size between min/max bounds
            matchTo (dict, optional): If provided, use this layout specification for all windows
            randomAll (bool, optional): If True, use random layout for all windows
            monitor (int, optional): Monitor index to use. If None, uses all monitors.
        """
        if matchTo is not None:
            layouts = [matchTo for _ in self.wnds]
        elif randomAll:
            layouts = [{"random": True} for _ in self.wnds]
        elif layouts is None:
            raise ValueError("Must provide layouts, matchTo, or set randomAll=True")
        elif len(layouts) != len(self.wnds):
            raise ValueError("Number of layouts must match number of windows")

        # Get monitors if not already cached
        monitors = screeninfo.get_monitors()
        monitors.sort(key=lambda m: not m.is_primary)
        
        # Filter to specific monitor if requested
        if monitor is not None:
            if monitor >= len(monitors):
                raise ValueError(f"Monitor index {monitor} out of range")
            monitors = [monitors[monitor]]

        # Track occupied spaces per monitor
        occupied_spaces = {i: [] for i in range(len(monitors))}  # Dict of monitor index to list of (x,y,w,h) tuples

        # Process each window with its layout
        for window, layout in zip(self.wnds, layouts):
            # Get preferred monitor
            target_monitor_idx = 0  # Default to primary
            target_monitor = monitors[0]
            
            if 'preferredMonitorList' in layout:
                for mon_idx in layout['preferredMonitorList']:
                    if mon_idx < len(monitors):
                        target_monitor = monitors[mon_idx]
                        target_monitor_idx = mon_idx
                        break

            # Calculate monitor work area
            mon_x = target_monitor.x + self.settings.monitor_margins_x
            mon_y = target_monitor.y + self.settings.monitor_margins_y
            mon_width = target_monitor.width - (2 * self.settings.monitor_margins_x)
            mon_height = target_monitor.height - (2 * self.settings.monitor_margins_y)

            # Apply custom constraints while respecting monitor bounds
            width = mon_width // 2  # Start with half monitor width as default
            height = mon_height // 2  # Start with half monitor height as default
            
            if 'maxwidth' in layout:
                width = min(width, layout['maxwidth'])
            if 'maxheight' in layout:
                height = min(height, layout['maxheight'])
            if 'minwidth' in layout:
                width = max(width, layout['minwidth'])
            if 'minheight' in layout:
                height = max(height, layout['minheight'])

            # Randomize size if requested
            if layout.get('random', False):
                import random
                min_w = layout.get('minwidth', width)
                max_w = layout.get('maxwidth', width)
                min_h = layout.get('minheight', height)
                max_h = layout.get('maxheight', height)
                width = random.randint(min_w, max_w)
                height = random.randint(min_h, max_h)

            # Try each monitor if preferred one is too crowded
            positioned = False
            for attempt_monitor_idx in range(len(monitors)):
                # Start with preferred monitor, then try others
                monitor_idx = (target_monitor_idx + attempt_monitor_idx) % len(monitors)
                current_monitor = monitors[monitor_idx]
                
                # Recalculate bounds for current monitor
                mon_x = current_monitor.x + self.settings.monitor_margins_x
                mon_y = current_monitor.y + self.settings.monitor_margins_y
                mon_width = current_monitor.width - (2 * self.settings.monitor_margins_x)
                mon_height = current_monitor.height - (2 * self.settings.monitor_margins_y)

                # Find non-overlapping position
                attempts = 0
                max_attempts = 100
                
                while attempts < max_attempts:
                    # Try random position within monitor bounds
                    x = mon_x + random.randint(0, mon_width - width)
                    y = mon_y + random.randint(0, mon_height - height)
                    
                    # Check for overlap with existing windows on this monitor
                    overlaps = False
                    for ox, oy, ow, oh in occupied_spaces[monitor_idx]:
                        if (x < ox + ow and x + width > ox and
                            y < oy + oh and y + height > oy):
                            overlaps = True
                            break
                    
                    if not overlaps:
                        occupied_spaces[monitor_idx].append((x, y, width, height))
                        positioned = True
                        break
                    attempts += 1
                
                if positioned:
                    break

            if not positioned:
                print("Warning: Could not find non-overlapping position for window on any monitor")
                continue

            # Apply layout
            utils.activate_wnd(window)
            if window.isMaximized:
                window.restore()
                
            window.resizeTo(width, height)
            window.moveTo(x, y)
            
            time.sleep(self.settings.elaspsed_time / 1000)