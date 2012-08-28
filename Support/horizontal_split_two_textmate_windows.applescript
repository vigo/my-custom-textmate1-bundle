tell application "Finder"
    set DesktopSize to bounds of window of desktop
    set DesktopWidth to item 3 of DesktopSize
    set DesktopHeight to item 4 of DesktopSize
end tell

tell application "TextMate"
    set WindowsList to (every window where visible is true)
    set n to count of WindowsList
    
    if n = 1 then return
    if n > 2 then
        say "sorry, max 2 windows allowed"
        return
    end if

    set the bounds of the first window to {0, 0, DesktopWidth, DesktopHeight / 2}
    set the bounds of the second window to {0, DesktopHeight / 2, DesktopWidth, DesktopHeight}
end tell
