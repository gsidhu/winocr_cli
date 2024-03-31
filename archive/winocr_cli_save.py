import winocr
import asyncio
import argparse
import concurrent.futures
from multiprocessing import freeze_support
from PIL import Image

def process_image(input_file, output_file, language):
    print("Processing for", input_file, "and", output_file)
    img = Image.open(input_file)
    ocr_result = recognize_pil_text(img, language)
    with open(output_file, "w") as output:
        output.write(ocr_result)
    print(f"OCR result saved to {output_file}")

async def ensure_coroutine(awaitable):
    return await awaitable

def recognize_pil_text(img, language="en"):
    return asyncio.run(ensure_coroutine(winocr.recognize_pil(img, lang=language))).text

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
                                     description='''
                WinOCR Command Line Interface
-------------------------------------------------------------------
* Performs OCR on PDFs and Images
* Supports Multiprocessing on several files in parallel
* Uses Windows native OCR API (available on Windows 10 and 11 only)
                                     ''',
                                     epilog='''
Example usage: winocr_cli.exe -i input_image.png input_pdf.pdf -o output_image.txt output_pdf.txt
                                     ''')
    parser.add_argument("-i", "--input", nargs='+', type=str, required=True, help="Input file path(s)")
    parser.add_argument("-l", "--language", type=str, default="en", help="Language for OCR (default: en)")
    parser.add_argument("-o", "--output", nargs='+', type=str, required=True, help="Output file path(s)")
    args = parser.parse_args()

    if len(args.input) != len(args.output):
        print("Error: Number of input files does not match number of output files.")
        return

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for input_file, output_file in zip(args.input, args.output):
            futures.append(executor.submit(process_image, input_file, output_file, args.language))
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    freeze_support()
    main()