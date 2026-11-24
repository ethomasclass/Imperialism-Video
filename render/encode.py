# Encode a folder of PNG frames to a video with Blender's own encoder (run by run_all.py):
#   blender -b --python render/encode.py -- <frames_dir> <out.mp4|out.mov> <alpha 0|1>
# H.264 at near-lossless quality for normal shots; QuickTime PNG (keeps transparency) for shots with alpha.
# Frames may be numbered from any start and may skip numbers (test renders); they are laid end to end in name order.
import bpy, os, sys

d, out, alpha = sys.argv[sys.argv.index('--') + 1:][:3]
files = sorted(f for f in os.listdir(d) if f.lower().endswith('.png'))
sc = bpy.context.scene
sc.render.fps = 30
img = bpy.data.images.load(os.path.join(d, files[0]))
sc.render.resolution_x, sc.render.resolution_y = img.size
sc.render.resolution_percentage = 100
se = sc.sequence_editor_create()
st = se.sequences.new_image('frames', os.path.join(d, files[0]), 1, 1)
for f in files[1:]:
    st.elements.append(f)
sc.frame_start, sc.frame_end = 1, len(files)
r = sc.render
r.use_sequencer = True
if alpha == '1':
    r.image_settings.file_format = 'FFMPEG'
    r.ffmpeg.format = 'QUICKTIME'
    r.ffmpeg.codec = 'PNG'
    r.image_settings.color_mode = 'RGBA'
else:
    r.image_settings.file_format = 'FFMPEG'
    r.ffmpeg.format = 'MPEG4'
    r.ffmpeg.codec = 'H264'
    r.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
    r.ffmpeg.ffmpeg_preset = 'GOOD'
    r.image_settings.color_mode = 'RGB'
r.ffmpeg.audio_codec = 'NONE'
sc.view_settings.view_transform = 'Standard'
base = os.path.join(os.path.dirname(out), '_enc_' + os.path.splitext(os.path.basename(out))[0] + '_')
r.filepath = base                                        # Blender appends the frame range; renamed below
bpy.ops.render.render(animation=True)
made = [f for f in os.listdir(os.path.dirname(out)) if f.startswith(os.path.basename(base))]
if os.path.exists(out):
    os.remove(out)
os.replace(os.path.join(os.path.dirname(out), made[0]), out)
print('ENCODED', out, len(files), 'frames')
