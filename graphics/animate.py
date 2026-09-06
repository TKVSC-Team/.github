from PIL import Image
import numpy as np

# 1. Load images and downscale
TARGET_SIZE = (400, 400)
bg = Image.open("BladesawIconBack.png").convert("RGBA").resize(TARGET_SIZE, Image.Resampling.LANCZOS)
blade_raw = Image.open("BladesawIconNoBack.png").convert("RGBA").resize(
    (int(TARGET_SIZE[0] * 0.85), int(TARGET_SIZE[1] * 0.85)), 
    Image.Resampling.LANCZOS
)

# 2. Instant transparency via NumPy
data = np.array(blade_raw)
is_black = (data[:, :, 0] < 40) & (data[:, :, 1] < 40) & (data[:, :, 2] < 40)
data[:, :, 3] = np.where(is_black, 0, 255)
blade = Image.fromarray(data)

# 3. Generate rotation frames
frames = []

# 60 frames across a 45° turn at 33ms (~30 FPS) = ~2 seconds per tooth (~16s full turn)
# Change to total_frames = 30 if you want ~1 second per tooth (~8s full turn)
total_frames = 60  
SECTOR_ANGLE = 360 / 8  # 45 degrees

for i in range(total_frames):
    angle = -(i / total_frames) * SECTOR_ANGLE
    rotated_blade = blade.rotate(angle, resample=Image.Resampling.BICUBIC)
    
    frame = bg.copy()
    offset = ((bg.width - rotated_blade.width) // 2, (bg.height - rotated_blade.height) // 2)
    frame.paste(rotated_blade, offset, rotated_blade)
    frames.append(frame.convert("RGB"))

# 4. Save GIF
frames[0].save(
    "spinning_bladesaw.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,  # Smooth 30 FPS playback
    loop=0,
    optimize=True
)

print("Done! Saved spinning_bladesaw.gif")