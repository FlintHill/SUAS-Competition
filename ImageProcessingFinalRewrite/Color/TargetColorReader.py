import Color.ColorMath as ColorMath

named_target_colors = (('black', (20,20,20)), ('white', (244,244,252)), ('gray', (128,128,128)), ('red', (228, 60, 76)), ('blue', (44,124,228)),  ('green', (68,180,92)), ('yellow', (252,220,52)), ('purple', (116,68,179)), ('brown', (236,204, 132)), ('orange', (236,132,52)))
target_colors = ((20,20,20), (244,244,252), (128,128,128), (228, 60, 76), (44,124,228), (68,180,92), (252,220,52), (116,68,179), (236,204,132), (236,132,52))
def get_closest_target_color(color):
    closest_color = ColorMath.get_closest_color_from_list(target_colors, color)
    return named_target_colors[target_colors.index(closest_color)][0]
    