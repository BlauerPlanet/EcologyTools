;cmd tzutil /l list all timezones
; %ComSpec% is an environment variable that typically expands to C:\Windows\System32\cmd.exe

#Requires AutoHotkey v2.0

TimeGui := Gui()
TimeGui.AddButton(, "change to UTC").OnEvent("Click", UTC_Click)
TimeGui.AddButton(, "change to Germany").OnEvent("Click", Ger_Click)
TimeGui.Show()

UTC_Click(*)
{
    Run A_ComSpec ' /c ""cmd.exe"  /c tzutil /s "UTC"'
}

Ger_Click(*)
{
    Run A_ComSpec ' /c ""cmd.exe"  /c tzutil /s "W. Europe Standard Time"'
}