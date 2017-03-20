import Color.ColorMath as ColorMath
import colorsys
from math import pi, sqrt

named_target_colors = (('black', (20,20,20)), ('white', (244,244,252)), ('gray', (128,128,128)), ('red', (228, 60, 76)), ('blue', (44,124,228)),  ('green', (68,180,92)), ('yellow', (252,220,52)), ('purple', (116,68,179)), ('brown', (236,204, 132)), ('orange', (236,132,52)))
target_colors = ((20,20,20), (244,244,252), (128,128,128), (228, 60, 76), (44,124,228), (68,180,92), (252,220,52), (116,68,179), (236,204,132), (236,132,52))
LIGHTNESS_WEIGHT = 1


def get_closest_target_color(color):
    closest_color = ColorMath.get_closest_color_from_list(target_colors, color)
    return named_target_colors[target_colors.index(closest_color)][0]
    
def get_closest_HSL_target_color(color):
    hsl_color = colorsys.rgb_to_hls(float(color[0])/255.0, float(color[1])/255.0, LIGHTNESS_WEIGHT * float(color[2])/255.0)
    hsl_color = (hsl_color[0], hsl_color[1], hsl_color[2])
    hsl_colors = []
    for i in range(0, len(target_colors)):
        iter_hsl_color = colorsys.rgb_to_hls(float(target_colors[i][0])/255.0, float(target_colors[i][1])/255.0, LIGHTNESS_WEIGHT * float(target_colors[i][2])/255.0)
        hsl_colors.append((iter_hsl_color[0], iter_hsl_color[1], iter_hsl_color[2]))
        
        
    sorted_hsl_colors = sorted(hsl_colors, key = lambda iter_hsl_color: sqrt((hsl_color[0]-iter_hsl_color[0])**2 + (hsl_color[1] - iter_hsl_color[1])**2 + LIGHTNESS_WEIGHT * (hsl_color[2] - iter_hsl_color[2])**2 ))
    closest_color = sorted_hsl_colors[0]#ColorMath.get_closest_color_from_list(hsl_colors, hsl_color)
    return named_target_colors[hsl_colors.index(closest_color)][0]
    
    
    '''
    closest_color_index = 0
    closest_color_angle_difference = abs(hsl_color[0] - colorsys.rgb_to_hls(target_colors[0][0], target_colors[0][1], target_colors[0][2])[0])
    for i in range(1, len(target_colors)):
        iter_hsl_color = colorsys.rgb_to_hls(target_colors[i][0], target_colors[i][1], target_colors[i][2])
        angle_diff = abs(hsl_color[0] - iter_hsl_color[0])
        if  angle_diff < closest_color_angle_difference:
            closest_color_angle_difference = angle_diff
            closest_color_index = i
    return named_target_colors[closest_color_index][0]'''
    

            
        
    