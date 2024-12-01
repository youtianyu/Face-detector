DIM objShell 
set objShell=wscript.createObject("wscript.shell") 
iReturn=objShell.Run("cmd.exe /C start_service.bat", 0, TRUE)  