from pdf2image import convert_from_path
import asyncio
import winocr
import os
from PIL import Image

async def ocr_this(input_file):
    output_folder = "temp_output"
    os.mkdir(output_folder)
    images = convert_from_path(input_file,
                               poppler_path=".\\poppler-24.02.0\\Library\\bin",
                               output_folder=output_folder,
                               grayscale=True)
    for filename in os.listdir(output_folder):
        img = Image.open(output_folder + "\\" + filename)
        ocr_result = (await winocr.recognize_pil(img, "en")).text
        with open(output_folder + "\\" + filename + ".txt", "w") as output:
            output.write(ocr_result)
        print(f"OCR result saved to {filename}.txt")
    combine_output(input_file)

def combine_output(output_file):
    output_folder = "temp_output"
    with open(output_file + ".txt", 'w+', encoding="utf-8") as f:
        for filename in os.listdir(output_folder):
            if ".txt" in filename:
                with open(output_folder + "\\" + filename) as temp_file:
                    f.write(temp_file.read())
                    f.write("\n")

if __name__ == "__main__":
    asyncio.run(ocr_this(input_file="test.pdf"))