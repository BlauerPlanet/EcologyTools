;cmd tzutil /l list all timezones
; %ComSpec% is an environment variable that typically expands to C:\Windows\System32\cmd.exe

#Requires AutoHotkey v2.0

;open window to change region (for decimal seperator, date format, ...)
Run "intl.cpl"

TimeGui := Gui()
TimeGui.AddButton(, "change to UTC").OnEvent("Click", UTC_Click)
TimeGui.AddButton(, "change to Germany").OnEvent("Click", Ger_Click)
TimeGui.Show()

; change timezone
UTC_Click(*)
{
    Run A_ComSpec ' /c ""cmd.exe"  /c tzutil /s "UTC"'
}

Ger_Click(*)
{
    Run A_ComSpec ' /c ""cmd.exe"  /c tzutil /s "W. Europe Standard Time"'
}