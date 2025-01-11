# ref: https://gist.github.com/Pagliacii/774ed5d3ea78a36cdb0754be6a25408d
# ref: https://github.com/soda92/toggle-icons/blob/main/Program.cs

from ctypes import windll, wintypes
import enum

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindoww
# HWND FindWindowW(
#   [in, optional] LPCWSTR lpClassName,
#   [in, optional] LPCWSTR lpWindowName
# );

FindWindow = windll.user32.FindWindowW
FindWindow.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR)
FindWindow.restype = wintypes.HWND

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindowexw
# HWND FindWindowExW(
#   [in, optional] HWND    hWndParent,
#   [in, optional] HWND    hWndChildAfter,
#   [in, optional] LPCWSTR lpszClass,
#   [in, optional] LPCWSTR lpszWindow
# );
FindWindowEx = windll.user32.FindWindowExW
FindWindowEx.argtypes = (
    wintypes.HWND,
    wintypes.HWND,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
)
FindWindowEx.restype = wintypes.HWND

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdesktopwindow
# HWND GetDesktopWindow();
GetDesktopWindow = windll.user32.GetDesktopWindow
GetDesktopWindow.restype = wintypes.HWND

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagew
# LRESULT SendMessageW(
#   [in] HWND   hWnd,
#   [in] UINT   Msg,
#   [in] WPARAM wParam,
#   [in] LPARAM lParam
# );
SendMessageW = windll.user32.SendMessageW
SendMessageW.argtypes = (wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
SendMessageW.restype = wintypes.INT


class GetWindow_Cmd(enum.Enum):
    GW_HWNDFIRST = 0
    GW_HWNDLAST = 1
    GW_HWNDNEXT = 2
    GW_HWNDPREV = 3
    GW_OWNER = 4
    GW_CHILD = 5
    GW_ENABLEDPOPUP = 6


def GetDesktopSHELLDLL_DefView():
    hShellViewWin = 0
    hWorkerW = 0

    hProgman = FindWindow("Progman", "Program Manager")
    hDesktopWnd = GetDesktopWindow()

    if hProgman != 0:
        hShellViewWin = FindWindowEx(hProgman, 0, "SHELLDLL_DefView", None)

        if hShellViewWin == 0:
            hWorkerW = FindWindowEx(hDesktopWnd, hWorkerW, "WorkerW", None)
            hShellViewWin = FindWindowEx(hWorkerW, 0, "SHELLDLL_DefView", None)
            while hShellViewWin == 0 and hWorkerW != 0:
                hWorkerW = FindWindowEx(hDesktopWnd, hWorkerW, "WorkerW", None)
                hShellViewWin = FindWindowEx(hWorkerW, 0, "SHELLDLL_DefView", None)
    return hShellViewWin


def ToggleDesktopIcons():
    WM_COMMAND = 0x111
    toggleDesktopCommand = 0x7402
    SendMessageW(GetDesktopSHELLDLL_DefView(), WM_COMMAND, toggleDesktopCommand, 0)


if __name__ == "__main__":
    ToggleDesktopIcons()
