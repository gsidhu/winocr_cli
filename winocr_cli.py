import winocr
import asyncio
import argparse
import concurrent.futures
from multiprocessing import freeze_support
from PIL import Image
import os
from pdf2image import convert_from_path

silent_mode = False
default_poppler_path = ".\\poppler-24.02.0\\Library\\bin"

def process_file(input_file, output_file, language, silent_mode=False):
    if input_file.lower().endswith(".pdf"):
        process_pdf(input_file, output_file, language, silent_mode)
    else:
        process_image(input_file, output_file, language, silent_mode)

def process_pdf(input_file, output_file, language, silent_mode=False):
    # check if Poppler is installed
    if not os.path.exists(default_poppler_path + "\\pdftoppm.exe"):
        if not silent_mode:
            print("\nError: Poppler not found. Please run winocr_cli.exe --setup to setup Poppler. Or recheck the provided Poppler path.")
        return
    if not silent_mode:
        print("Processing for", input_file, "and", output_file)
    output_folder = "temp_output"
    os.mkdir(output_folder)
    images = convert_from_path(input_file,
                               poppler_path=default_poppler_path,
                               output_folder=output_folder,
                               grayscale=True)
    for filename in os.listdir(output_folder):
        img = Image.open(output_folder + "\\" + filename)
        ocr_result = recognize_pil_text(img, language)
        with open(output_folder + "\\" + filename + ".txt", "w") as output:
            output.write(ocr_result)
        if not silent_mode:
            print(f"OCR result saved to {filename}.txt")
    combine_output(output_file, silent_mode)

def combine_output(output_file, silent_mode=False):
    output_folder = "temp_output"
    with open(output_file, 'w+', encoding="utf-8") as f:
        for filename in os.listdir(output_folder):
            if ".txt" in filename:
                with open(output_folder + "\\" + filename) as temp_file:
                    f.write(temp_file.read())
                    f.write("\n")
    if not silent_mode:
        print("Saved final output to", output_file)

def process_image(input_file, output_file, language, silent_mode=False):
    if not silent_mode:
        print("Processing for", input_file, "and", output_file)
    img = Image.open(input_file)
    ocr_result = recognize_pil_text(img, language)
    with open(output_file, "w") as output:
        output.write(ocr_result)
    if not silent_mode:
        print(f"OCR result saved to {output_file}")

async def ensure_coroutine(awaitable):
    return await awaitable

def recognize_pil_text(img, language="en"):
    return asyncio.run(ensure_coroutine(winocr.recognize_pil(img, lang=language))).text

def setup_poppler(silent_mode):
    poppler_download_path = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip"
    if not silent_mode:
        print("Downloading Poppler from", poppler_download_path)
    import urllib.request
    urllib.request.urlretrieve(poppler_download_path, "poppler.zip")
    if not silent_mode:
        print("Extracting Poppler")
    import zipfile
    with zipfile.ZipFile("poppler.zip", 'r') as zip_ref:
        zip_ref.extractall()
    if not silent_mode:
        print("Poppler setup complete")
    

def main():
    global silent_mode
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
                                     description='''
                WinOCR Command Line Interface
-------------------------------------------------------------------
* Performs OCR on PDFs and Images
* Supports Multiprocessing on several files in parallel
* Uses Windows native OCR API (available on Windows 10 and 11 only)

NOTE: Run winocr_cli.exe --setup to setup Poppler for PDF processing
                                     ''',
                                     epilog='''
Example usage: winocr_cli.exe -i input_image.png input_pdf.pdf -o output_image.txt output_pdf.txt
                                     ''')
    parser.add_argument("-i", "--input", nargs='*', type=str, help="Input file path(s)")
    parser.add_argument("-l", "--language", type=str, default="en", help="Language for OCR (default: en)")
    parser.add_argument("-o", "--output", nargs='*', type=str, help="Output file path(s)")
    parser.add_argument("-s", "--silent", action='store_true', help="Run operations silently. Does not print any output to console.")
    parser.add_argument("--poppler_path", type=str, default=default_poppler_path, help="Path to Poppler (default: %(default)s)")
    
    setup_group = parser.add_mutually_exclusive_group()
    setup_group.add_argument("--setup", action='store_true', help="Setup Poppler for PDF processing")
    
    args = parser.parse_args()
    silent_mode = args.silent

    if args.setup:
        setup_poppler(silent_mode)
        return

    if len(args.input) != len(args.output):
        print("Error: Number of input files does not match number of output files.")
        return
    
    for input_file in args.input:
        if not (input_file.lower().endswith(".pdf") or input_file.lower().endswith(".png") or input_file.lower().endswith(".jpg") or input_file.lower().endswith(".jpeg")):
            print("Error: winocr_cli can process only PDF, PNG and JPG/JPEG files. Please check the input files.")
            return

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for input_file, output_file in zip(args.input, args.output):
            futures.append(executor.submit(process_file, input_file, output_file, args.language, silent_mode))
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    freeze_support()
    main()