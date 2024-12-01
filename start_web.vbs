DIM objShell 
set objShell=wscript.createObject("wscript.shell") 
iReturn=objShell.Run("cmd.exe /C start_web.bat", 0, TRUE)  