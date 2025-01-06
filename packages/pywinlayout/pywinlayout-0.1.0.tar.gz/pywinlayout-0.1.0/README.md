# PyWinLayout
PyWinLayout is a Python library for managing and arranging windows on multiple monitors in Windows. It provides various layout options including grid layouts, middle stacking, and custom moodboard arrangements.

## Features

- Multiple layout options:
  - Simple grid layout (e.g., 2x3 grid)
  - Middle stack with offset
  - Custom grid across multiple monitors
  - Moodboard (custom positioning with overlap prevention)
- Window selection by:
  - Window title patterns
  - Process name patterns
  - Monitor location
- Multi-monitor support
- Configurable margins and constraints
- Window size constraints
- Automatic window activation

## Installation

```bash
pip install pywinlayout
```

## Quick Start

```python
from pywinlayout import PyWinLayout

# Arrange all windows in a 2x3 grid
PyWinLayout.allWindows().simpleGrid("2x3")

# Arrange Chrome windows in a middle stack
PyWinLayout.matchProcs(["chrome.exe"]).middleStack(offset=30, direction="right")

# Arrange specific apps in a custom grid across monitors
layout = PyWinLayout.matchProcs(["code.exe", "chrome.exe", "slack.exe"])
layout.grid("2x2")
```

## Layout Options

### Simple Grid
Arranges windows in a grid pattern on a single monitor:
```python
# Arrange in 2x3 grid (2 rows, 3 columns)
PyWinLayout.allWindows().simpleGrid("2x3")
```

### Middle Stack
Arranges windows with the first window centered and others stacked behind:
```python
# Stack windows to the right with 20px offset
PyWinLayout.allWindows().middleStack(offset=20, direction="right")

# Available directions: "right", "left", "up", "down"
```

### Multi-monitor Grid
Arranges windows across multiple monitors in a grid pattern:
```python
# 2x2 grid across all available monitors
PyWinLayout.allWindows().grid("2x2")
```

### Moodboard
Custom window arrangement with overlap prevention:
```python
layouts = [
    {
        "minwidth": 800,
        "maxwidth": 1200,
        "minheight": 600,
        "maxheight": 800,
        "preferredMonitorList": [0],
        "random": True
    }
]
PyWinLayout.allWindows().moodboard(layouts=layouts)
```

## Window Selection

Select windows by different criteria:

```python
# By window title (supports wildcards)
PyWinLayout.matchWnds(["Chrome*", "Visual Studio Code"])

# By process name
PyWinLayout.matchProcs(["chrome.exe", "code.exe"])

# By monitor
PyWinLayout.allWindowsOnMonitor(0)  # Primary monitor
```

## Configuration

Customize behavior with settings:

```python
from pywinlayout import Settings

settings = Settings(
    monitor_margins_x=10,      # Horizontal margin from monitor edges
    monitor_margins_y=10,      # Vertical margin from monitor edges
    elaspsed_time=1000,       # Delay between window movements (ms)
    min_wnd_width=100,        # Minimum window width
    min_wnd_height=100,       # Minimum window height
    max_wnd_width=-1,         # Maximum window width (-1 for no limit)
    max_wnd_height=-1         # Maximum window height (-1 for no limit)
)

layout = PyWinLayout.allWindows(settings=settings)
```

## Requirements
- Windows operating system
- Python 3.6+
- Dependencies:
  - pygetwindow
  - screeninfo
  - psutil (optional, for process information)
  - pywin32 (optional, for process information)

## License
[MIT](https://github.com/ZackaryW/pywinlayout/blob/main/LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer
This project is not affiliated with or endorsed by Microsoft.

This project uses AI to help piece together past code snippets and work around solutions.