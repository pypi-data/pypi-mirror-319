#Requires AutoHotkey v2.0
#SingleInstance Force

TraySetIcon "{resources}\tool.ico"

EDITOR := "powershell {edit.ps1}"

Media_Prev::
{
    Send "!{Left}"
}

Media_Next::
{
    Send "!{Right}"
}

#!R::
{
    Run "soda-ahk.exe -e"
}

#K::
{
    Send "!{F4}"
}

#I::
{
    if !WinExist("ahk_exe chrome.exe") {
        Run "C:\Program Files\Google\Chrome\Application\chrome.exe"
    }
    if WinWait("ahk_exe chrome.exe", , 3) {
        WinActivate
    }
}

#!H::
{
    if !WinExist("ahk_exe hh.exe") {
        Run "{AutoHotkey.chm}"
        WinWait("ahk_exe hh.exe", , 3)
    }
    else {
        WinActivate("ahk_exe hh.exe")
        WinMaximize("ahk_exe hh.exe")
    }
}

#!P::
{
    Run "ms-settings:colors"
}

#!E::
{
    Run Format("{1} {WindowsTerminal.ahk}", EDITOR), , "Hide"
}

; Fn: SC163/VKFF ; [TODO] Not effective
VKFF & E::
{
    Run Format("{1} {WindowsTerminal.ahk}", EDITOR), , "Hide"
}

#S::
{
    if !WinExist("Settings") {
        Run "ms-settings:appsfeatures-app"
    }
    WinWait "Settings", , 3
    WinActivate
    Sleep 200
    Send "{Tab}"
}

; Run Terminal: Ctrl+Alt+T
^!T::
{
    Run "wt.exe"
}

#Esc::
{
    if !WinExist("ahk_exe procexp64.exe") {
        Run "procexp64.exe"
    }
    if WinWait("ahk_exe procexp64.exe", , 3) {
        WinActivate
        WinMaximize
    }
}

; Hide/Show Desktop icons: Win+Alt+D, Win+Ctrl+D
; See https://github.com/soda92/toggle-icons for source code
#!D::
{
    Run "{toggle-icons.exe}"
}

#^D::
{
    Run "{toggle-icons.exe}"
}

; Ctrl + Shift + S
#+S::
{
    Send "{PrintScreen}"
}


#!K::
{
Run '"{desktop}\BGI.exe - Shortcut.lnk"'
}

#HotIf WinActive("ahk_exe BGI.exe")
f::
{
Send "{Enter}"
}

#HotIf WinActive("ahk_exe BGI.exe")
v::
{
Send "{Enter}"
}
