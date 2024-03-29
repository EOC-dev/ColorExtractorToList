import cv2 #OpenCV takes the image and converts it into a numpy array
import numpy as np
from collections import OrderedDict #This is used to construct the Color Lookup Table
import argparse #These two used so the script can use arguments to specify input image
import os

#This section sets up getting user arguments and using imread to convert image into an array that we will loop through:

parser = argparse.ArgumentParser()

parser.add_argument('-I', type=str, default='NULL_IMAGE', help='The name of the input image file')

args = parser.parse_args()

#Read the image file using OpenCV (needs to be in same directory)
img = cv2.imread(args.I)


#Now, the main processing can begin (assuming user entered the image correctly):

#Check if the image was read successfully
if img is None:
  print('\nError: Image could not be read pls check filename and extension!')
else:
  #Extract the filename and extension of the input image file
  filename, file_ext = os.path.splitext(args.I)

  #Create the names of the output files by prefixing the filenames with the input filename
  color_list_file = '{}_ColorList.txt'.format(filename)
  color_table_file = '{}_ColorLookupTable.txt'.format(filename)

  #Extract the width and height of the image using numpy
  height, width, _ = img.shape #Numpy returns a tuple, that why the _ is there since we just need height and width

  #Create a Lookup Table to store each unique color that appears in the image using pythons OrderedDict
  unique_colors = OrderedDict()

  #Create an empty list to store the hexadecimal string outputs for each pixel color value calculated in the following for loops
  hex_strings = []

  #Loop through the image per pixel and extract rbg info for each in row major form
  for y in range(height):
    for x in range(width):
      #Extract the RGB values of the pixel
      r, g, b = img[y, x]

      #Convert the RGB values to a hexadecimal string
      #For some reason it needs to be b,g,r to write the value in RRBBGG format (needed for the VHDL code)
      hex_string = '{:02X}{:02X}{:02X}'.format(b, g, r)

      #Append each hex string per pixel to the list of hexadecimal strings
      hex_strings.append(hex_string)

      #Append each unique color value found in image to the Color LookupTable
      if hex_string not in unique_colors:
        unique_colors.update({hex_string: len(unique_colors)})

  #Save the index values of the colors to a .txt file
  with open(color_list_file, 'w') as f:
    for L, hex_string in enumerate(hex_strings):
      #Look up the index value of the color in the Color Lookup Table
      index = unique_colors[hex_string]

      #Convert the index value to a hexadecimal string
      #Since I was using the matalb script for the project, I programmed the VHDL to index from 1 to match, thus the +1
      hex_index = hex(index+1) # If indexing from 0, remove the +1

      #Remove the "0x" prefix from the hexadecimal string and capitalize the hexadecimal letters
      #The way it formats the hex string is different from what we need for VHDL to know it's a hex string literal
      #This needed formating is done later in the f.write statements
      hex_index = hex_index[2:].upper().zfill(1)

     
      #This if-else statement ensures that the last line printed does not have the comma or the newline
      #This is specifically because in VHDL the last line can't have the comma. This way the user doesn't have
      #To delete it manually.
      if L == len(hex_strings) - 1:
          # If this is the last iteration of the loop, write the line without the comma or the newline
          f.write('x\"{}\"'.format(hex_index))
      else:
          f.write('x\"{}\",\n'.format(hex_index))
    

  #Same concept for the Color Lookup Table
  with open(color_table_file, 'w') as f:
    for i, (color, index) in enumerate(unique_colors.items()):
      if i == len(unique_colors) - 1:
          #If this is the last iteration of the loop, write the line without the comma or the newline
          f.write('x\"{}\" --{}'.format(color, index+1))
      else:
          f.write('x\"{}\", --{}\n'.format(color, index+1)) # If indexing from 0, remove the +1

