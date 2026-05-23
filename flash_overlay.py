"""Fullscreen overlay flash — camera-flash effect on all monitors.
Zero dependencies (ctypes only). No focus steal, no taskbar entry.
"""
import ctypes
from ctypes import wintypes
import sys
import time

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

WS_POPUP = 0x80000000
WS_EX_LAYERED = 0x80000
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TOPMOST = 0x8
WS_EX_TOOLWINDOW = 0x80
LWA_ALPHA = 0x2
BRUSHES = {"white": 0, "black": 4}

UINT_PTR = ctypes.c_ulonglong
LONG_PTR = ctypes.c_longlong

WNDPROC = ctypes.WINFUNCTYPE(LONG_PTR, wintypes.HWND, wintypes.UINT,
                              UINT_PTR, LONG_PTR)
MonitorCB = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC,
                                ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, UINT_PTR, LONG_PTR]
user32.DefWindowProcW.restype = LONG_PTR


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


@WNDPROC
def _wndproc(hwnd, msg, wparam, lparam):
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)


def flash(count=3, dark_ms=100, light_ms=400, alpha=100, mode="black"):
    rects = []

    @MonitorCB
    def _enum_cb(hmon, hdc, rect, data):
        r = rect.contents
        rects.append((r.left, r.top, r.right, r.bottom))
        return True

    user32.EnumDisplayMonitors(None, None, _enum_cb, 0)
    if not rects:
        return

    hinst = kernel32.GetModuleHandleW(None)
    cls_name = "ClaudeFlashV3"

    brush = BRUSHES.get(mode, 4)

    wc = WNDCLASSW()
    wc.lpfnWndProc = _wndproc
    wc.hInstance = hinst
    wc.hbrBackground = gdi32.GetStockObject(brush)
    wc.lpszClassName = cls_name

    atom = user32.RegisterClassW(ctypes.byref(wc))
    if not atom:
        return

    try:
        for i in range(count):
            hwnds = []
            for left, top, right, bottom in rects:
                hwnd = user32.CreateWindowExW(
                    WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
                    atom, None, WS_POPUP,
                    left, top, right - left, bottom - top,
                    None, None, hinst, None
                )
                if hwnd:
                    user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)
                    user32.ShowWindow(hwnd, 5)
                    hwnds.append(hwnd)

            time.sleep(dark_ms / 1000.0)

            for hwnd in hwnds:
                user32.DestroyWindow(hwnd)

            if i < count - 1:
                time.sleep(light_ms / 1000.0)
    finally:
        user32.UnregisterClassW(atom, hinst)


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    dark_ms = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    light_ms = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    alpha = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    mode = sys.argv[5] if len(sys.argv) > 5 else "black"
    flash(count, dark_ms, light_ms, alpha, mode)
