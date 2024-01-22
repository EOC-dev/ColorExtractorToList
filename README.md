# ColorExtractorToList
A python script that uses opencv to extract color values from an image and output them into a simple list and color lookup table.

## Installation and setup

First setup python and virtual environments on your machine, then install the dependencies:

* Opencv
* Numpy

## Usage

This is a command line tool that can be ran with the following after cd'ing into the working directory:

py OpenCVColorExtractor.py -I [ImageName].png

running the script will place two .txt files in the same folder it was ran in -- one is a list of all the colors in the image, and the other is a list of every unique color in that image.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

