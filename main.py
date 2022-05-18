from PIL import Image
import numpy as np
import matplotlib.pyplot as plt



print("Name of input file: ", end='')
inp = Image.open(input())
inp = inp.convert("RGB")
width = inp.width
height = inp.height



print(f"Image Size: {width} x {height}\n")

valid = False
while not valid:
    print("Number of points to read: ", end='')
    num_points = int(input())
    if num_points <= 2 or num_points > width:
        continue

    print("Degree of polynomial: ", end='')
    degree = int(input())

    print("Scaling factor (0 is leftmost, n is rightmost): ", end='')
    scale = int(input())
    
    valid = True
        


print("\n\n") #spacer
mid_height = round(height / 2)

x_positions = []
r_values = []
g_values = []
b_values = []

for i in range(num_points):
    point_x = (2 * i + 1) * (width / (num_points * 2))
    point_x = int(point_x)
    point_x_scaled = (2 * i + 1) * (scale / (num_points * 2))
    x_positions.append(point_x_scaled)
    
    rgb_value = inp.getpixel( (point_x, mid_height) )
    r_values.append(rgb_value[0])
    g_values.append(rgb_value[1])
    b_values.append(rgb_value[2])
    
    #print(f"RGB of ({point_x}, {mid_height}) is {rgb_value}.")



print("\n\n")

r_coefficients = np.polyfit(x_positions, r_values, degree)
g_coefficients = np.polyfit(x_positions, g_values, degree)
b_coefficients = np.polyfit(x_positions, b_values, degree)

r_polynomial = ""
g_polynomial = ""
b_polynomial = ""

for i in range(degree + 1):
    if i == 0:
        r_polynomial += f"The red component is given by {r_coefficients[i]:.30f}x^{degree}"
        g_polynomial += f"The green component is given by {g_coefficients[i]:.30f}x^{degree}"
        b_polynomial += f"The blue component is given by {b_coefficients[i]:.30f}x^{degree}"
    elif i == degree:
        r_polynomial += f" + {r_coefficients[i]:.30f}"
        g_polynomial += f" + {g_coefficients[i]:.30f}"
        b_polynomial += f" + {b_coefficients[i]:.30f}"
    elif i == degree - 1:
        r_polynomial += f" + {r_coefficients[i]:.30f}x"
        g_polynomial += f" + {g_coefficients[i]:.30f}x"
        b_polynomial += f" + {b_coefficients[i]:.30f}x"
    else:
        r_polynomial += f" + {r_coefficients[i]:.30f}x^{degree - i}"
        g_polynomial += f" + {g_coefficients[i]:.30f}x^{degree - i}"
        b_polynomial += f" + {b_coefficients[i]:.30f}x^{degree - i}"

print(r_polynomial)
print(g_polynomial)
print(b_polynomial)



##new_image = []
##for row in range(10):
##    image_row = []
##    for i in range(scale):
##        pixel = [0, 0, 0]
##        pixel[0] = round(min(max(np.poly1d(r_coefficients)(i), 0), 255))
##        pixel[1] = round(min(max(np.poly1d(g_coefficients)(i), 0), 255))
##        pixel[2] = round(min(max(np.poly1d(b_coefficients)(i), 0), 255))
##        image_row.append(pixel)
##    new_image.append(image_row)
##
##new_image = np.array(new_image, dtype=np.uint8)
##new_image = Image.fromarray(new_image)
##new_image.show()



#c/o harvey
print()

r_error = 0
g_error = 0
b_error = 0

for i in range(width):
    point_x_scaled = (2 * i + 1) * (scale / (width * 2))
    
    rgb_value = inp.getpixel( (i, mid_height) )
    
    r = min(max(np.poly1d(r_coefficients)(point_x_scaled), 0), 255)
    g = min(max(np.poly1d(g_coefficients)(point_x_scaled), 0), 255)
    b = min(max(np.poly1d(b_coefficients)(point_x_scaled), 0), 255)
    
    r_error += abs(rgb_value[0] - r)
    g_error += abs(rgb_value[1] - g)
    b_error += abs(rgb_value[2] - b)
    
print(f"Average error R channel: {r_error / width} / 255")
print(f"Average error G channel: {g_error / width} / 255")
print(f"Average error B channel: {b_error / width} / 255")






#grayscale colorizing
grayscale = np.asarray(Image.open("grayscale.png"))
grayscale = grayscale.tolist()

compressed_grayscale = []
for row in grayscale:
    compressed_row = []
    for pixel in row:
        compressed_row.append(pixel * scale / 255)
    compressed_grayscale.append(compressed_row)

colorized = []
for row in compressed_grayscale:
    colorized_row = []
    for pixel in row:
        colorized_pixel = [0 for _ in range(3)]
        colorized_pixel[0] = min(max(np.poly1d(r_coefficients)(pixel), 0), 255)
        colorized_pixel[1] = min(max(np.poly1d(g_coefficients)(pixel), 0), 255)
        colorized_pixel[2] = min(max(np.poly1d(b_coefficients)(pixel), 0), 255)
        
        colorized_row.append(colorized_pixel)
        
    colorized.append(colorized_row)

colorized = np.array(colorized, dtype=np.uint8)
colorized = Image.fromarray(colorized)
colorized.show()
