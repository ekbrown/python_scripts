"""Python function to extract text out of PDF files, whether they are already indexed or not.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
"""

import os, pytesseract, re, shutil, subprocess, time

try:
    import Image
except ImportError:
    from PIL import Image

def escaper(x):
    """Helper function to escape problematic characters in file pathways; add more if needed"""
    x = x.replace(" ", "\ ")
    x = x.replace("(", "\(")
    x = x.replace(")", "\)")
    return x

def is_indexed(filename, pathway_dir_xpdf_tools):
    """Takes a pathway to a PDF file and returns whether it's indexed as boolean value"""
    basename, file_ext = os.path.splitext(filename)
    assert file_ext.lower() == ".pdf", "You gotta supply 'is_indexed' with a PDF file; check that file extension homez!"
    filename = escaper(filename)
    pathway = os.path.join(pathway_dir_xpdf_tools, "pdffonts")
    to_run = f"{pathway} {filename}"
    result = subprocess.run(to_run, shell=True, stdout = subprocess.PIPE)
    output = re.search(r"[- ]{80,}\\n\w+", str(result.stdout))
    return bool(output)

def get_txt_pdf(pathway_tesseract_executable, pathway_dir_pdf_files, pathway_dir_xpdf_tools, language):
    """Python function to extract text from PDF files, whether or not those files are already indexed. It produces TXT files for each PDF file, and return the Python value Nothing (a void function).
    param pathway_tesseract_executable: string, pathway to Tesseract executable;
    param pathway_dir_pdf_files: string, pathway to directory with PDF files;
    param pathway_dir_xpdf_tools: string, pathway to directory with xPDF command-line tools;
    param language: string, Tesseract code indicating the human language in the PDF files (cf. https://github.com/tesseract-ocr/tessdata); the language model must have been previously installed in the "tessdata" directory, e.g., "tesseract/4.1.0/share/tessdata" (default is "eng" [English])
    return value: Nothing (a void function)
    """

    # specify pathway to Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = pathway_tesseract_executable

    # change into directory with PDF files and get filenames
    # os.chdir("/Users/ekb5/Documents/corpus_law/sample_files")
    os.chdir(pathway_dir_pdf_files)
    filenames = sorted([f for f in os.listdir() if bool(re.search(r"\.pdf", f, flags=re.I))])


    # loop over file
    for f in filenames:

        # is the current file already indexed?
        cur_indexed = is_indexed(f, pathway_dir_xpdf_tools)

        # escape characters in file pathway
        f = escaper(f)

        # already indexed
        if cur_indexed:
            print(f"The file {f} seems to be already indexed!")
            pathway = os.path.join(pathway_dir_xpdf_tools, "pdftotext")
            to_run = f"{pathway} -layout -nopgbrk {f}"
            subprocess.run(to_run, shell=True)

        # not yet indexed; the file must be OCRed
        else:
            print(f"The file {f} doesn't seem to be indexed yet. Gonna OCR it now...")

            # create temporary directory into which images files can be saved
            temp_dir = "temp_dir_to_delete_very_soon"
            if os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)
            os.mkdir(temp_dir)

            # convert each page of unindexed PDF file as separate image files
            pathway = os.path.join(pathway_dir_xpdf_tools, "pdftoppm")

            to_run = f"{pathway} -r 300 -gray {f} ./{temp_dir}/"
            subprocess.run(to_run, shell=True)

            # loop over images files, extracting text and adding to TXT file on hard drive
            images = sorted([i for i in os.listdir(temp_dir) if re.search(r"\.pgm", i)])
            basename, file_ext = os.path.splitext(f)
            with open(basename + ".txt", mode = "w", encoding = "utf8") as outfile:

                count = 0
                for i in images:
                    count += 1

                    print(f"\rworking on page {count} of {len(images)}", end = "")
                    image_path = temp_dir + "/" + i

                    # the OCR magic happens here
                    txt = pytesseract.image_to_string(Image.open(image_path), lang = language)

                    # write current page's text to TXT file on hard drive
                    outfile.write(txt + "\n")

                # delete temporary directory
                shutil.rmtree(temp_dir)

            print()


### test the function
pathway_tesseract_executable = "/usr/local/bin/tesseract"
# pathway_dir_pdf_files = "/Users/ekb5/Documents/help/Korean_Liahona/infiles"
pathway_dir_pdf_files = "/Users/ekb5/Documents/corpus_law/sample_files"
pathway_dir_xpdf_tools = "/Users/ekb5/xpdf-tools-mac-4.01.01/bin64"
language = "eng"

start = time.time()
get_txt_pdf(pathway_tesseract_executable, pathway_dir_pdf_files, pathway_dir_xpdf_tools, language)
print("\nThe script took", time.time() - start, "seconds to run.")
