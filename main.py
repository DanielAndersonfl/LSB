from PIL import Image as pilImage


# get image
def get_image(image_dir):
    # Line 3 is taken from google to get my predictive functions working. idk specifically what it does tbh.
    my_image: pilImage.Image = pilImage.open(image_dir)
    # my_image.show()
    return my_image


def get_image_data(image):
    # Get all of the pixel Data and store it in a list with format [(R,G,B,A), (R,G,B,A),...].
    image_data = list(image.getdata())
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
    meme_ratio = max_length / message_length
    # print(f'Max_len / Mes_len: [{meme_ratio}]\nmes_len:{message_length}')
    # get the difference between max_length and message_length
    length_difference = max_length - message_length
    # Compare message length to max length
    is_too_long = max_length < message_length
    if is_too_long:
        # Inform user of the issue with their message length, provide solutions to fix the issue on their end.
        # Return 'is_too_long'
        print(f'Please shorten the message or start over and select a larger image.', end="")
        print(f'you need to remove {abs(length_difference)}')
        return is_too_long
    # return 'is_too_long'
    return is_too_long


# Create a new list with the same format but store the data in binary.
def image_data_to_bin(in_list, img_mode):
    # Create an empty list.
    image_bin_data = []
    # Iterate through the inputted list.
    for pixel in in_list:
        if img_mode == 'RGBA':
            # Iterate through the rgba values, convert them to binary and store in image_bin_data list.
            for x in range(0, 4):
                image_bin_data.append(int_to_bin(pixel[x]))
        elif img_mode == 'RGB':
            # Iterate through the rgba values, convert them to binary and store in image_bin_data list.
            for x in range(0, 3):
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


# Insert the message into the lsb' of the binary image data. return the modified image data.
def insert_message(bin_message, binary_image_data):
    # Create a copy of the input list to not modify the original.
    encoded_image_data = binary_image_data
    # Index of the message to be encoded.
    message_index = 0
    # Replace the last index of each lsb with message data.
    for x in range(len(encoded_image_data)):
        # Replace the last index in the string with appropriate message data.
        encoded_image_data[x] = replace_index_in_string(7, encoded_image_data[x], bin_message[message_index])
        try:
            bin_message[message_index + 1]
            message_index += 1
        except IndexError:
            message_index = 0
    # Return the encoded image data
    return encoded_image_data


# Replace index in string
def replace_index_in_string(index, string, new_val):
    new_string = ""
    for x in range(len(string)):
        if x != index:
            new_string += string[x]
        else:
            new_string += new_val
    return new_string


# Convert bin to integer
def bin_to_ascii(bin_string):
    n = int(bin_string, 2)
    return n


# Convert list from bin to integer
def encoded_image_data_to_integer(encoded_image_data):
    converted_to_integer = []
    for x in encoded_image_data:
        converted_to_integer.append(bin_to_ascii(x))
    return converted_to_integer


# Perform the actions required to encode the message into the image data.
def encode_image(image_dir, messages):
    # Get image
    image = get_image(image_dir)
    # Get image data.
    image_data = get_image_data(image)
    # get bin image data
    bin_image_data = image_data_to_bin(image_data, image.mode)
    # get bin message
    bin_message = text_to_bin(messages)
    print(f'Bin message data: {bin_message[:80]}')
    # Get the maximum length of the message
    max_message_length = get_max_message_length(image)
    # Check if the message length is too long.
    is_too_long = check_length_validity(max_message_length, messages)
    # only proceed if the message fits in the image.
    if not is_too_long:
        encoded_image_data = insert_message(bin_message, bin_image_data)
        encoded_rgba = encoded_image_data_to_integer(encoded_image_data)
        tuple_encoded_rgba = convert_to_tuple_list(encoded_rgba, image.mode)
        print(f'Image data:         {image_data[:9]}')
        print(f'Encoded RGBa:       {tuple_encoded_rgba[:9]}')
        encoded_image = draw_encoded_image(image, tuple_encoded_rgba)
        __EID__ = get_image_data(encoded_image)
        print(f'__EID__:            {__EID__[:9]}')
        if image.mode == 'RGBA':
            encoded_image.save('encoded.png')
            with pilImage.open('encoded.png') as __IMG__:
                __EID__ = get_image_data(__IMG__)
                print(f'__EID__POST:        {__EID__[:9]}')
        elif image.mode == 'RGB':
            encoded_image.save('encoded.jpg')
            with pilImage.open('encoded.jpg') as __IMG__:
                __EID__ = get_image_data(__IMG__)
                print(f'__EID__POST:        {__EID__[:9]}')


# Convert encoded image data into RGB/RGBA Tuples.
def convert_to_tuple_list(encoded_image_data, image_mode):
    rgb_tuple_list = []
    if image_mode == 'RGBA':
        x = 0
        while x <= len(encoded_image_data) - 4:
            rgb_tuple_list.append((encoded_image_data[x], encoded_image_data[x+1],
                                   encoded_image_data[x+2], encoded_image_data[x+3]))
            x += 4
        return rgb_tuple_list
    elif image_mode == 'RGB':
        x = 0
        while x <= len(encoded_image_data) - 3:
            rgb_tuple_list.append((encoded_image_data[x], encoded_image_data[x + 1],
                                   encoded_image_data[x + 2]))
            x += 3
        return rgb_tuple_list


# Replace the image with the new encoded image
def draw_encoded_image(image, encoded_image_data):
    width, height = image.size
    new_image = pilImage.new(image.mode, (width, height))
    pix = 0
    for y in range(height):
        for x in range(width):
            # print(f'Length EID:{pix}/{len(encoded_image_data)}')
            # print(f'[y:{y}/{height}]\n[x:{x}/{width}]\n[RGB:{encoded_image_data[pix]}]')
            new_image.putpixel((x, y), encoded_image_data[pix])
            pix += 1
    # new_image.show()
    return new_image


# Get the binary message from 'bin_image_data'
def retrieve_bin_message(bin_image_data):
    msg = ''
    for x in bin_image_data:
        msg = 1
    return msg


if __name__ == '__main__':
    # get message
    message = get_message()
    print(f'------------------------------------------PNG------------------------------------------')
    encode_image('location_pin.png', message)
    print(f'------------------------------------------JPG------------------------------------------')
    encode_image('img_lights.jpg', message)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTING FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print(list_to_bin(image_data))
# print(get_max_message_length(my_image))
# print(int_to_bin())
# print(text_to_bin('dog'))
