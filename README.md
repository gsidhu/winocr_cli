# winocr_cli: WinOCR Command Line Interface
A minimal command line application for converting images and PDFs to text using Windows native OCR APIs.

The application is just a wrapper around the [winocr](https://github.com/GitHub30/winocr) Python package.

## How to use it
1. **Download the executable:** Download the `winocr_cli.exe` file from the [Releases](https://github.com/gsidhu/winocr_cli/releases) section of this repository.
2. **Open Command Prompt or PowerShell:** Navigate to the directory where you downloaded the `winocr_cli.exe` file.
3. **Run the command:** Use the following command syntax:
```
winocr_cli.exe -l "en" -i \path\to\image.png -o \path\to\output.txt
```
- Replace `\path\to\image.png` with the path to your input image file.
- Replace `\path\to\output.txt` with the path where you want to save the output text file.
- Optionally, you can specify the language parameter `-l` (default is "en").
- To process multiple input and output files, you can specify multiple pairs of input-output using the same command format:
```
winocr_cli.exe -l "en" -i image1.png image2.png -o output1.txt output2.txt
```

Once the command is executed, the output text file(s) will be generated at the specified location(s).

## How to build it from source 
1. **Clone the repository.**
2. **Install dependencies:** Navigate to the cloned directory and install the required dependencies.
3. **Run the script:** Navigate to the `src` directory and run the script using Python:
```
python winocr_cli.py -l "en" -i \path\to\image.png -o \path\to\output.txt
```

### Dependencies
- `winocr`
- `pillow` (PIL)

## Note
- Ensure that the input image file exists and is accessible from the command line.
- The application bundles all necessary dependencies, so there's no need to install them separately.
- The executable might trigger security warnings on your machine. Feel free to bypass them to use the app. Or build it yourself from source.
- Language support is constrained by the languages available on your Windows installation.

## Contributing
Contributions are welcome! If you'd like to contribute to winocr_cli, please submit a pull request detailing the changes you made.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
