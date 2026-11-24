# The render runner. Started by RENDER_WINDOWS.bat / RENDER_MAC.command through Blender itself:
#   blender -b --python render/run_all.py -- [shot names or groups ...]
# Reads render/shots.json, renders each shot's frames at full quality with a fresh Blender process (the same Blender that
# runs this script), then encodes the frames to a video in renders/ with Blender's own encoder (no ffmpeg needed).
# Everything resumes: frames already on disk are skipped by the set scripts, and a shot whose video exists is skipped.
# Delete renders/<shot>.mp4 (or .mov) to render a shot again; delete frames/<shot>/ too to start it from scratch.
import bpy, json, os, shutil, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EP = os.path.join(ROOT, 'ep1')
FRAMES = os.path.join(ROOT, 'frames')
RENDERS = os.path.join(ROOT, 'renders')
LOGS = os.path.join(ROOT, 'logs')
for d in (FRAMES, RENDERS, LOGS):
    os.makedirs(d, exist_ok=True)
BLENDER = bpy.app.binary_path
SHOTS = json.load(open(os.path.join(ROOT, 'render', 'shots.json'), encoding='utf-8'))['shots']
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
want = set(argv)


def picked(s):
    return not want or s['name'] in want or s.get('group') in want


def log(msg):
    line = time.strftime('%H:%M:%S ') + msg
    print(line, flush=True)
    with open(os.path.join(LOGS, 'run_all.log'), 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def pngs(d):
    """the folder under d holding the most PNG frames (some modes write into a subfolder)"""
    best, n = d, 0
    for r, _, fs in os.walk(d):
        k = sum(1 for f in fs if f.lower().endswith('.png'))
        if k > n:
            best, n = r, k
    return best, n


def video_path(s):
    return os.path.join(RENDERS, s['name'] + ('.mov' if s.get('alpha') else '.mp4'))


def render(s):
    out = os.path.join(FRAMES, s['name'])
    os.makedirs(out, exist_ok=True)
    script = os.path.join(EP, 'blender', s['script'])
    args = [BLENDER, '-b', '--python-exit-code', '1', '--python', os.path.join(ROOT, 'render', 'utf8.py'), '--python', script, '--', out] + [str(a) for a in s.get('args', [])]
    env = dict(os.environ)
    env.update({k: str(v) for k, v in s.get('env', {}).items()})
    t = time.time()
    log(f"RENDER {s['name']}: {s['script']} {' '.join(str(a) for a in s.get('args', []))} {s.get('env', {})}")
    with open(os.path.join(LOGS, s['name'] + '.log'), 'w', encoding='utf-8') as lf:
        rc = subprocess.call(args, env=env, stdout=lf, stderr=subprocess.STDOUT, cwd=os.path.join(EP, 'blender'))
    d, n = pngs(out)
    log(f"  done in {(time.time() - t) / 60:.1f} min, exit {rc}, {n} frames")
    if rc != 0 or n == 0:
        log(f"  PROBLEM: see logs/{s['name']}.log (the next run will retry this shot)")
        return False
    for src, dst in s.get('copy', []):                     # e.g. a board picture another shot needs
        sp = os.path.join(out, src)
        if os.path.exists(sp):
            os.makedirs(os.path.dirname(os.path.join(EP, dst)), exist_ok=True)
            shutil.copyfile(sp, os.path.join(EP, dst))
            log(f'  copied {src} -> ep1/{dst}')
    return True


def encode(s):
    d, n = pngs(os.path.join(FRAMES, s['name']))
    if n < 2 or s.get('still'):
        return True                                        # stills stay as PNGs (pushed with the frames folder)
    enc = os.path.join(ROOT, 'render', 'encode.py')
    rc = subprocess.call([BLENDER, '-b', '--python', enc, '--', d, video_path(s), '1' if s.get('alpha') else '0'],
                         stdout=open(os.path.join(LOGS, s['name'] + '_encode.log'), 'w', encoding='utf-8'), stderr=subprocess.STDOUT)
    ok = rc == 0 and os.path.exists(video_path(s))
    log(f"  ENCODE {os.path.basename(video_path(s))}: {'ok' if ok else 'FAILED, see logs'}")
    return ok


log(f'Blender {bpy.app.version_string}  ({BLENDER})  shots asked for: {sorted(want) or "all"}')
if bpy.app.version >= (4, 2, 0):
    log('STOP: these scripts need Blender 4.0 or 4.1 (4.2 replaced the EEVEE renderer). See README.md.')
    sys.exit(1)
todo = [s for s in SHOTS if picked(s)]
log(f'{len(todo)} shots to check')
fails = 0
for i, s in enumerate(todo, 1):
    if fails >= 8:
        log('STOPPED after 8 failures in a row: send Claude the logs/<shot>.log of the first one.')
        break
    done_marker = os.path.join(FRAMES, s['name'], 'DONE')
    if s.get('still') and os.path.exists(done_marker):
        continue
    if not s.get('still') and os.path.exists(video_path(s)):
        log(f"[{i}/{len(todo)}] {s['name']}: video exists, skipped")
        continue
    log(f"[{i}/{len(todo)}] {s['name']}")
    if render(s):
        fails = 0
        if encode(s) and s.get('still'):
            open(done_marker, 'w').close()
    else:
        fails += 1
log('ALL DONE. Commit and push the renders/ folder (and frames/ for the stills) with GitHub Desktop.')
