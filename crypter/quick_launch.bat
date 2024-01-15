@echo off
setlocal

REM Recherche de l'emplacement de python.exe dans le PATH
for %%i in (python.exe) do (
    set python_exec=%%~$PATH:i
    if defined python_exec (
        set python_exec_found=true
        goto :execute_script
    )
)

REM Si python.exe n'est pas trouvé, affichez un message d'erreur
if not defined python_exec_found (
    echo Python n'a pas été trouvé dans le PATH.
    echo Assurez-vous que Python est installé et ajouté au PATH.
    pause
    exit /b
)

:execute_script
REM Exécutez votre script Python en passant tous les arguments du script batch
"%python_exec%" "%~dp0crypter.pyw" %*

endlocal
