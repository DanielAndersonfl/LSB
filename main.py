from PIL import Image as pilImage


def get_image_data():
    # Line 3 is taken from google to get my predictive functions working. idk specifically what it does tbh.
    my_image: pilImage.Image = pilImage.open("location_pin.png")
    # Get all of the pixel Data and store it in a list with format [(R,G,B,A), (R,G,B,A),...].
    image_data = list(my_image.getdata())
    return image_data


# Get the message from the text file 'message.txt'
def get_message():
    # Open the 'message.txt' file as msg
    with open('message.txt', 'r') as msg:
        # turn the empty 'message' variable into a variable containing the message to be hidden.
        message = msg.read()
    # Return the message.
    return message


# Determine the max length of characters an image can be based off of the dimensions of the image being used.
def get_max_message_length(image):
    # Get the width of the image.
    image_width = image.size[0]
    # Get the height of the image.
    image_height = image.size[1]
    # Get the mode of the image(RGB or RGBA).
    image_mode = image.mode
    # Perform the calculations based off of image width, height and mode.
    if image_mode == 'RGBA':
        max_char_length = int(image_width * image_height * 4 // 8)
    if image_mode == 'RGB':
        max_char_length = int(image_width * image_height * 3 // 8)
    # Return the maximum character length a message can be.
    return max_char_length


# Confirm that the message is not too long. And return length difference.
def check_length_validity(max_length, message):
    # Get length of the message.
    message_length = len(message)
    # Compare message length to max length
    is_too_long = max_length <= message_length
    # get the difference between max_length and message_length
    length_difference = max_length - message_length
    # return a tuple with a bool for if the message is too long, and the length difference.
    return tuple(is_too_long, length_difference)


# Create a new list with the same format but store the data in binary.
def list_to_bin(in_list):
    # Create an empty list.
    image_bin_data = []
    # Iterate through the inputted list.
    for pixel in in_list:
        # Iterate through the rgba values, convert them to binary and store in image_bin_data list.
        for x in range(0, 4):
            image_bin_data.append(int_to_bin(pixel[x]))
    # Return the image_bin_data list.
    return image_bin_data


# Convert inputted text string to it's binary value.
def text_to_bin(text):
    # Iterate through the inputted string and convert the characters to their unicode code point representation.
    # and assign those values to a new string, return the string.
    binary_value = ''.join(format(ord(i), '08b') for i in text)
    return binary_value


# Convert inputted integer to binary
def int_to_bin(num):
    # convert to 8 digit binary and store in binary_value
    binary_value = '{0:08b}'.format(num)
    # return binary_value
    return binary_value



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTING FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print(list_to_bin(image_data))
# print(get_max_message_length(my_image))
# print(int_to_bin())
# print(text_to_bin('dog'))