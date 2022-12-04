# Native Original NES Resolution for context
nes_wResolution = 256
nes_hResolution = 240

# Resolution Width
wScreen = 1280
# Resolution Height will always be a multiple of the native nes_hResolution for consistency
hScreen = nes_hResolution*3

# Sprite Scaling
sprite_size = hScreen/15
# Grid Size
wGrid = wScreen/sprite_size
hGrid = hScreen/sprite_size
