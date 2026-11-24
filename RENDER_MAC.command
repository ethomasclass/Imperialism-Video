#!/bin/bash
# Renders every shot in render/shots.json with Blender 4.1 (resumes where it stopped). Double-click to run.
# From Terminal you can pass shot names or groups:  ./RENDER_MAC.command boards coldopen
cd "$(dirname "$0")"
for B in "/Applications/Blender 4.1.app/Contents/MacOS/Blender" "/Applications/Blender4.1.app/Contents/MacOS/Blender" \
         "/Applications/Blender 4.0.app/Contents/MacOS/Blender" "/Applications/Blender.app/Contents/MacOS/Blender"; do
  [ -x "$B" ] && BLENDER="$B" && break
done
if [ -z "$BLENDER" ]; then echo "Could not find Blender 4.1 in /Applications. Edit this file and set BLENDER."; read -n1; exit 1; fi
"$BLENDER" -b --python render/run_all.py -- "$@"
echo; echo "Finished. Now open GitHub Desktop, commit the new files in renders/ and push."; read -n1
