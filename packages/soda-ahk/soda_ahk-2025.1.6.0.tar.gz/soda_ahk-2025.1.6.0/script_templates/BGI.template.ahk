#Requires AutoHotKey v2.0
#SingleInstance Force

TraySetIcon "{resources}\mouse.ico"

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

#!J::
{
	Run "python.exe {cursor}\stop.py"
}

Loop {
  if WinExist("ahk_exe BGI.exe")  {
    if (!FileExist("{cursor}\running")){
      Run "soda-ahk-cursor.exe",,"Hide"
    }
  } else {
    if (FileExist("{cursor}\running")){
		Run "soda-ahk-cursor.exe --stop"
    }
  }
  Sleep 1000
}
