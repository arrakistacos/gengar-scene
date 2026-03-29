#!/bin/bash
# Automated Google Lens image analysis

export DISPLAY=:0

# Open Google Lens in new window
google-chrome --new-window "https://lens.google.com" &
sleep 4

# Click on "Upload image" button area
xdotool mousemove 960 540
xdotool click 1

sleep 2

# Type the file path
xdotool type "/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"
sleep 1
xdotool key Return

sleep 10

# Take screenshot of results (give time for analysis)
gnome-screenshot -f /home/freeman/.openclaw/workspace/gengar-project/lens_results.png 2>/dev/null || xdotool key Print

echo "Google Lens analysis complete - check lens_results.png"
