import argparse
import asyncio
import winocr
from PIL import Image

async def ocr_this(input_file, language):
    img = Image.open(input_file)
    return (await winocr.recognize_pil(img, language)).text

async def main():
    parser = argparse.ArgumentParser(description="WinOCR Image OCR Command Line Application")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("-l", "--language", type=str, default="en", help="Language for OCR (default: en)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    args = parser.parse_args()

    result = await ocr_this(args.input, args.language)
    with open(args.output, "w") as output_file:
        output_file.write(result)
    print(f"OCR result saved to {args.output}")

if __name__ == "__main__":
    asyncio.run(main())