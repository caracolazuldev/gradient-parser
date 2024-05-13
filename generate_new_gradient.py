import os
import subprocess
import xml.etree.ElementTree as ET

from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor


# Function to calculate the color distance between two colors
def calculate_color_distance(color1, color2):
	delta_e = delta_e_cie2000(convert_rgb_to_lab(color1),convert_rgb_to_lab(color2))
	if hasattr(delta_e, 'item'):
		return delta_e.item()
	elif hasattr(delta_e, 'tolist'):
		return delta_e.tolist()[0]
	else:
		return delta_e


def convert_rgb_to_lab(rgb_color):
	return convert_color(rgb_color, LabColor)

def valid_rgb_color(color):
	if not color or len(color) != 7 or color[0] != '#':
		print("Invalid color code:", color)
		return None
	
	try:
		color_rgb = sRGBColor.new_from_rgb_hex(color)
		# Continue with your color processing logic here
		return color_rgb
	except Exception as e:
		print("Error processing color:", e)
		return None

# Function to calculate the new color based on the color distance from the original base colors
def calculate_new_color(original_color, org_base_one, org_base_two, new_base_one, new_base_two):
	original_color_rgb = valid_rgb_color(original_color)
	org_base_one_rgb = sRGBColor.new_from_rgb_hex(org_base_one)
	org_base_two_rgb = sRGBColor.new_from_rgb_hex(org_base_two)
	
	# Calculate the distances from the original color to the original base colors
	distance_to_org_base_one = calculate_color_distance(original_color_rgb, org_base_one_rgb)
	distance_to_org_base_two = calculate_color_distance(original_color_rgb, org_base_two_rgb)
	
	# Calculate the interpolation weights based on the distances
	total_distance = distance_to_org_base_one + distance_to_org_base_two
	weight_one = 1 - distance_to_org_base_two / total_distance
	weight_two = 1 - distance_to_org_base_one / total_distance
	
	# Interpolate between the new base colors based on the weights
	new_base_one_rgb = sRGBColor.new_from_rgb_hex(new_base_one)
	new_base_two_rgb = sRGBColor.new_from_rgb_hex(new_base_two)
	
	new_color_rgb = (
		weight_one * new_base_one_rgb.rgb_r + weight_two * new_base_two_rgb.rgb_r,
		weight_one * new_base_one_rgb.rgb_g + weight_two * new_base_two_rgb.rgb_g,
		weight_one * new_base_one_rgb.rgb_b + weight_two * new_base_two_rgb.rgb_b
	)
	 
	new_color = sRGBColor(*new_color_rgb)
	
	return new_color.get_rgb_hex()

# # Example usage
# org_base_one = '#FF0000'
# org_base_two = '#00FF00'
# new_base_one = '#0000FF'
# new_base_two = '#FFFF00'
# original_color = '#336699'

# new_color = calculate_new_color(original_color, org_base_one, org_base_two, new_base_one, new_base_two)
# print(f"New Color: {new_color}")


# Function to map original HEX colors to new HEX colors based on color distances
def map_colors(original_colors, org_base_one, org_base_two, new_base_one, new_base_two):
	color_mapping = {}
	for color in original_colors:
		new_color = calculate_new_color(color, org_base_one, org_base_two, new_base_one, new_base_two)
		color_mapping[color] = new_color

	return color_mapping

def replace_colors_in_svg(input_svg, output_svg, color_mapping):
	tree = ET.parse(input_svg)
	root = tree.getroot()

	# Find all elements with a fill attribute
	for elem in root.iter():
		if 'fill' in elem.attrib:
			fill_color = elem.attrib['fill']
			if fill_color in color_mapping:
				elem.attrib['fill'] = color_mapping[fill_color]

	tree.write(output_svg)

# Main function
def main():
	base_one = os.getenv('BASE_ONE', '#FF0000')  # Default value if BASE_ONE is not set
	base_two = os.getenv('BASE_TWO', '#0000FF')  # Default value if BASE_TWO is not set

	# Invoke the first script (main.py) to generate the output
	output = subprocess.check_output(["python", "main.py"]).decode('utf-8')

	# Filter out non-empty lines between the specified markers
	start_marker = "All Fill Colors in the SVG file:"
	end_marker = "Base Colors of the Gradient (if present):"
	found_start = False
	original_colors = []
	original_base_one = None
	original_base_two = None

	for line in output.split('\n'):
		line = line.strip()  # Remove leading and trailing whitespaces
		
		if not line:  # Skip empty lines
			continue
		
		if found_start and end_marker not in line:
			original_colors.append(line)
		
		if start_marker in line:
			found_start = True
   
		if end_marker in line:
			found_start = False
		
		if "Base Color 1:" in line:
			original_base_one = line.split(":")[1].strip()
		elif "Base Color 2:" in line:
			original_base_two = line.split(":")[1].strip()


	# #DEBUG
	# print("Filtered Original Colors:")
	# print("\n".join(original_colors))
	# print(f"Original Base Color 1: {original_base_one}")
	# print(f"Original Base Color 2: {original_base_two}")

	color_mapping = map_colors(original_colors, original_base_one, original_base_two, base_one, base_two)

	#DEBUG
	print("Color Mapping:")	
	for key, value in color_mapping.items():
		print(f"Original Color: {key} -> New Color: {value}")

	input_svg = 'input.svg'
	output_svg = 'output.svg'

	replace_colors_in_svg(input_svg, output_svg, color_mapping)

if __name__ == '__main__':
	main()
