import pygetwindow as gw

def get_pid_from_hwnd(hwnd):
    """
    Get the process ID given the handle of a window.

    Args:
        hwnd (int or gw.Win32Window): The handle of the window. If it is an instance of gw.Win32Window, its handle will be extracted.

    Returns:
        int or None: The process ID of the window, or None if an error occurred.
    """
    if not isinstance(hwnd, int):
        assert isinstance(hwnd, gw.Win32Window)
        hwnd = hwnd._hWnd

    try:
        import win32process
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def activate_wnd(wnd: gw.BaseWindow):
    """
    Activates the given window if it is not already active.

    Args:
        wnd (gw.Window): The window to activate.

    Returns:
        None

    Raises:
        None
    """
    try:
        if wnd.isActive:
            return
        wnd.activate()
    except gw.PyGetWindowException:
        pass


def get_monitor_dimensions(monitor):
    """Get standardized monitor dimensions from monitor object or index.
    
    Args:
        monitor (Union[screeninfo.Monitor, int, None]): Monitor specification
        
    Returns:
        tuple: (width, height, x, y) of the monitor
    """
    import screeninfo
    
    if isinstance(monitor, screeninfo.Monitor):
        return (monitor.width, monitor.height, monitor.x, monitor.y)
    
    # Get default or specified monitor
    monitors = screeninfo.get_monitors()
    if monitor is None:
        monitor = 0
    elif monitor >= len(monitors):
        raise ValueError(f"Monitor index {monitor} out of range")
    mon = monitors[monitor]
    return (mon.width, mon.height, mon.x, mon.y)

def apply_window_constraints(width, height, settings):
    """Apply min/max constraints to window dimensions.
    
    Args:
        width (int): Desired window width
        height (int): Desired window height
        settings (Settings): Settings object with constraints
        
    Returns:
        tuple: (constrained_width, constrained_height)
    """
    if settings.max_wnd_width > 0:
        width = min(width, settings.max_wnd_width)
    if settings.max_wnd_height > 0:
        height = min(height, settings.max_wnd_height)
    width = max(width, settings.min_wnd_width)
    height = max(height, settings.min_wnd_height)
    return (width, height)
    

def is_window_on_monitor(window, monitor_dimensions):
    """Check if a window's center point falls within a monitor's dimensions.
    
    Args:
        window (Win32Window): Window to check
        monitor_dimensions (tuple): Monitor dimensions as (width, height, x, y)
        
    Returns:
        bool: True if window's center is within monitor area
    """
    if window.width == 0 or window.height == 0:
        return False
        
    # Calculate window center point
    wnd_center_x = window.left + (window.width // 2)
    wnd_center_y = window.top + (window.height // 2)
    
    # Unpack monitor dimensions
    width, height, x, y = monitor_dimensions
    
    # Check if window center is in monitor area
    return (x <= wnd_center_x <= x + width and 
            y <= wnd_center_y <= y + height)
    

def get_all_visible_windows():
    """Get all visible windows."""
    wnds = []
    for wnd in gw.getAllWindows():
        if wnd.width == 0 or wnd.height == 0:
            continue
        if not wnd.title:
            continue
        wnds.append(wnd)
    return wnds

