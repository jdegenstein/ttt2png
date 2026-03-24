# SolidWorks PDF to PNG Converter

A simple command-line utility that converts SolidWorks PDF drawings into perfectly centered, unwarped 1600x900 PNG images. 

SolidWorks exports PDFs as vector graphics. This tool renders them at a high resolution to maintain crisp dimension lines and text, scales them proportionally, and places them on a standard 1600x900 white canvas.

## Prerequisites

* **Python:** 3.10 or newer
* **uv:** The extremely fast Python package and project manager. [uv installation](https://docs.astral.sh/uv/getting-started/installation)

## Installation

Because this tool is packaged with a `pyproject.toml`, you can install it globally as a standalone command-line application using `uv tool`. This handles all dependencies in an isolated environment and automatically configures your system path.

1. Clone or download this repository.
2. Open your terminal and navigate to the root directory (where the `pyproject.toml` file is located).
3. Run the following command:

```bash
uv tool install .
```

Once the installation is complete, the `pdf2png` command will be available globally on your system.

## Usage

You can run this tool in any folder on your computer that contains PDF files. It has two modes: interactive and batch.

### 1. Interactive Mode
Navigate to a folder with your PDFs and run the base command:

```bash
uv tool run pdf2png
```
The tool will automatically detect the first PDF in the folder and offer it as the default input. Press `Enter` to accept the defaults, or type a specific filename. It will output a PNG with the same base name.

### 2. Batch Mode
To convert an entire folder of PDFs at once without any manual prompts, use the `--batch` flag:

```bash
uv tool run pdf2png --batch
```
This will scan the current directory, process every `.pdf` file it finds, and save the corresponding `.png` files right next to them.

### Help Menu
To view the available options from the command line:

```bash
uv tool run pdf2png --help
```
