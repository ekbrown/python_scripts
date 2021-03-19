"""
Python script to OCR .pdf files with Google's Tesseract and save the text in .txt files

Note: Before running this script, you must have downloaded and installed Tesseract and ImageMagick (and GhostScript, if using a Mac), and the Pillow Python module.
"""

#%%
# load up the workhorses
import os, re
from subprocess import call
import pytesseract
from PIL import Image

# SPECIFY PATHWAY TO TESSERACT EXECUTABLE
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'

# get .pdf filenames
# SPECIFY PATHWAY TO DIRECTORY WITH .PDF FILES
os.chdir('/Users/ekb5/Documents/LING_360')
filenames = [i for i in os.listdir() if re.search(r'\.pdf$', i, flags=re.I)]

#%%
# loop over .pdf files
for filename_pdf in filenames:

    # progress report
    print("Working on", filename_pdf)

    # create .jpg filename for current .pdf file
    barename = re.sub(r'\.pdf$', '', filename_pdf, flags=re.I)
    filename_jpg = barename +  ".jpg"
    resolution = re.search(r"\d+", filename_pdf).group(0)

    # convert from .pdf to .jpg
    # Thanks to Jeremy Browne for help with this line
    call(["convert", "-density", resolution,  filename_pdf, filename_jpg])

    # OCR .jpg and extract text to Python string
    text = pytesseract.image_to_string(Image.open(filename_jpg))

    # write text to .txt file
    with open(barename + '.txt', 'w') as fout:
        fout.write(text)

print("All done!")
