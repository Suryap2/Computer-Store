# Open the image file in binary mode
with open('KeyBoard.png', 'rb') as image_file:
    # Read the binary data
    binary_data = image_file.read()

# Print the binary data (This will be a long string of binary data)
print(binary_data)
