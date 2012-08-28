-- property parent : application "TextMate"

tell application "Finder"
    set DesktopSize to bounds of window of desktop
    set DesktopWidth to item 3 of DesktopSize
    set DesktopHeight to item 4 of DesktopSize
end tell

tell application "TextMate"
    set WindowsList to (every window where visible is true)
    set n to count of WindowsList
    
    if n = 1 then return
    if n > 4 then
        say "sorry, max 4"
        return
    end if
    
    set blockSize to DesktopWidth / 3
    set blockSizeW to DesktopWidth / 2
    set blockSizeH to DesktopHeight / 2
    
    if n = 2 then
        set the bounds of the first window to {0, 0, blockSizeW, DesktopHeight}
        set the bounds of the second window to {blockSizeW, 0, DesktopWidth, DesktopHeight}
    end if
    
    if n = 3 then
        set the bounds of the first window to {0, 0, blockSize, DesktopHeight}
        set the bounds of the second window to {blockSize, 0, (blockSize * 2), DesktopHeight}
        set the bounds of the third window to {(blockSize * 2), 0, DesktopWidth, DesktopHeight}
    end if
    
    if n = 4 then
        set the bounds of the first window to {0, 0, blockSizeW, blockSizeH}
        set the bounds of the second window to {blockSizeW, 0, DesktopWidth, blockSizeH}
        set the bounds of the third window to {0, blockSizeH, blockSizeW, DesktopHeight}
        set the bounds of the fourth window to {blockSizeW, blockSizeH, DesktopWidth, DesktopHeight}
    end if
end tell