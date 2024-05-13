
import math
import xml.etree.ElementTree as ET

# Function to extract all fill colors from SVG file
def extract_fill_colors(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    fill_colors = set()

    for elem in root.iter():
        if 'fill' in elem.attrib:
            fill_color = elem.attrib['fill']
            fill_colors.add(fill_color)

    return fill_colors

import math

# Function to convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to calculate the distance between two colors in RGB space
def color_distance(color1, color2):
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    return math.sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)

# Function to identify two base colors of a gradient based on color position
def identify_gradient_base_colors(fill_colors):
    color_positions = {}
    for i, color in enumerate(fill_colors):
        if color in color_positions:
            color_positions[color].append(i)
        else:
            color_positions[color] = [i]

    # Calculate the average position of each color in the gradient
    avg_positions = {color: sum(positions) / len(positions) for color, positions in color_positions.items()}

    # Sort colors based on their average position
    sorted_colors = sorted(avg_positions.items(), key=lambda x: x[1])

    base_colors = [color for color, _ in sorted_colors[:2]]

    return base_colors

# Main function to analyze SVG file
def analyze_svg(svg_file):
    fill_colors = extract_fill_colors(svg_file)
    base_colors = identify_gradient_base_colors(fill_colors)

    print("All Fill Colors in the SVG file:")
    for color in fill_colors:
        print(color)

    print("\nBase Colors of the Gradient (if present):")
    for idx, color in enumerate(base_colors, start=1):
        print(f"Base Color {idx}: {color}")

# Specify the path to your SVG file
svg_file_path = "input.svg"

# Analyze the SVG file
analyze_svg(svg_file_path)

# You can run this script by replacing `"path/to/your/svg/file.svg"` with the actual path to your SVG file. The script will extract all fill colors used in the SVG file, sort and analyze them, and identify the two base colors of a gradient if present.

# Feel free to customize the script further based on your specific requirements or the structure of your SVG file. Let me know if you need any further assistance or modifications!