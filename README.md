# American Imperialism, Ep 1: render kit

The Blender scenes for "The Pitch Meeting", packed so they render on a computer with a graphics card. The scripts are
the same ones as in the main repo (`15minhistorystyle/projects/American_Imperialism`), with the same folder layout.

## One-time setup
1. Install **Blender 4.1** (not 4.2 or later: 4.2 replaced the EEVEE renderer these scenes are built for). Get it from
   https://download.blender.org/release/Blender4.1/ . It installs next to any other Blender and doesn't touch it.
   - Windows: the `.msi` installs to `C:\Program Files\Blender Foundation\Blender 4.1\`, which the launcher finds.
     (Or unzip the portable `.zip` next to this folder.)
   - Mac: drag it into Applications and rename it **Blender 4.1**.
2. Clone this repo with GitHub Desktop.

## Rendering
- Double-click **RENDER_WINDOWS.bat** (Windows) or **RENDER_MAC.command** (Mac). It renders every shot in
  `render/shots.json` at full size and full frame rate, then turns each shot's frames into a video in `renders/`.
- It resumes: close it any time; the next run skips finished videos and finished frames.
- To render only some shots, run from a terminal with names or groups: `boards`, `coldopen`, `pitchroom`, `maps`,
  `sets` (e.g. `RENDER_WINDOWS.bat boards coldopen`). Run `boards` first: other shots use the pictures it makes.
- Progress: `logs/run_all.log`. A shot that fails writes `logs/<shot>.log`; the next run retries it.
- Frames go to `frames/` (not committed, it's large). Videos go to `renders/`.

## Sending the results back
Open GitHub Desktop, commit the new files in `renders/` (and the changed board pictures in `ep1/build/pitchroom/`),
and push. Claude pulls them into the episode, composites the transitions and assembles the chapters.

## Shot list
`render/shots.json`. Shots marked `"untested": true` haven't rendered a frame in the cloud tests yet; they get checked
there before the whole list is run.
