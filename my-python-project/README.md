# My Python Project

## Overview
This project provides a simple utility to convert PNG images to PDF files using Python. It leverages the `fpdf` library for PDF generation and the `Pillow` library for image handling.

## Installation
To get started, you need to install the required dependencies. You can do this using pip. Run the following command in your terminal:

```
pip install -r requirements.txt
```

## Usage
To use the `png_to_pdf` function, you need to import it from the `png_to_pdf` module. Here’s a quick example:

```python
from src.png_to_pdf import png_to_pdf

# Convert a PNG image to a PDF
png_to_pdf("path/to/your/image.png", "path/to/output/file.pdf")
```

### Parameters
- `png_path`: The file path of the PNG image you want to convert.
- `pdf_path`: The file path where the output PDF will be saved.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.