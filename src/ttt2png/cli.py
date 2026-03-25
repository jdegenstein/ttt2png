import pymupdf
from PIL import Image
import os
import glob
import argparse


def check_overwrite(filepath):
    """Prompts the user if the target file already exists."""
    if os.path.exists(filepath):
        while True:
            # Changed prompt to (Y/n) to indicate Yes is default
            ans = (
                input(f"  -> Warning: '{filepath}' already exists. Overwrite? (Y/n): ")
                .strip()
                .lower()
            )

            # Added empty string '' to the 'yes' condition
            if ans in ["y", "yes", ""]:
                return True
            elif ans in ["n", "no"]:
                return False
            else:
                print("     Please answer 'y' or 'n'.")
    return True


def convert_pdf_to_png(pdf_path, output_png_path, target_width=1600, target_height=900):
    try:
        # 1. Open the PDF file
        doc = pymupdf.open(pdf_path)

        # Warn if PDF has more than 1 page
        if doc.page_count > 1:
            print(
                f"  -> Warning: '{pdf_path}' has {doc.page_count} pages. Only the first page will be converted."
            )

        # Assuming the drawing is on the first page (index 0)
        page = doc.load_page(0)

        # Warn if PDF page is not close to 16:9 aspect ratio
        rect = page.rect
        width = rect.width
        height = rect.height

        if height != 0:
            aspect_ratio = width / height
            target_ratio = target_width / target_height  # 1600 / 900 = 1.777...

            # Allow a small tolerance of 0.05
            if abs(aspect_ratio - target_ratio) > 0.05:
                print(
                    f"  -> Warning: Page aspect ratio is {aspect_ratio:.2f} ({width:.0f}x{height:.0f}), which is not close to 16:9 ({target_ratio:.2f})."
                )

        # 2. Render the page to an image at a high resolution
        zoom = 4.0
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # 3. Convert the PyMuPDF pixmap into a Pillow Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 4. Scale the image down to fit within 1600x900, maintaining aspect ratio
        img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)

        # 5. Create a blank white canvas of exactly 1600x900
        final_image = Image.new("RGB", (target_width, target_height), "white")

        # 6. Paste the scaled drawing into the center of the white canvas
        paste_x = (target_width - img.width) // 2
        paste_y = (target_height - img.height) // 2
        final_image.paste(img, (paste_x, paste_y))

        # 7. Save the final PNG
        final_image.save(output_png_path, "PNG")
        print(f"  -> Success! Saved to {output_png_path}")

    except Exception as e:
        print(f"  -> An error occurred: {e}")
    finally:
        # Clean up
        if "doc" in locals():
            doc.close()


def main():
    parser = argparse.ArgumentParser(
        description="Convert SolidWorks / CAD PDFs to 1600x900 PNGs."
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Convert all PDFs in the current directory without prompting.",
    )
    args = parser.parse_args()

    # --- BATCH MODE ---
    if args.batch:
        print("--- Batch Conversion Mode ---")
        pdfs = glob.glob("*.pdf")

        if not pdfs:
            print("No PDF files found in the current directory.")
            return

        print(f"Found {len(pdfs)} PDF(s). Starting conversion...\n")

        for pdf in pdfs:
            base_name = os.path.splitext(pdf)[0]
            output_png = f"{base_name}.png"
            print(f"Converting '{pdf}'...")

            # Warn if a png file is going to be overwritten
            if not check_overwrite(output_png):
                print(f"  -> Skipped '{pdf}'.\n")
                continue

            convert_pdf_to_png(pdf, output_png)
            print()  # Add an empty line for readability between batch files

        print("Batch conversion complete!")
        return

    # --- INTERACTIVE MODE ---
    print("--- SolidWorks PDF to PNG Converter ---\n")

    pdfs = glob.glob("*.pdf")
    default_pdf = pdfs[0] if pdfs else None

    if default_pdf:
        pdf_prompt = f"Enter input PDF filename [{default_pdf}]: "
        pdf_input = input(pdf_prompt).strip()
        input_pdf = pdf_input if pdf_input else default_pdf
    else:
        input_pdf = input("Enter input PDF filename: ").strip()
        while not input_pdf:
            print("An input filename is required.")
            input_pdf = input("Enter input PDF filename: ").strip()

    if not os.path.exists(input_pdf):
        print(f"\nError: The file '{input_pdf}' was not found.")
        return

    base_name = os.path.splitext(input_pdf)[0]
    default_png = f"{base_name}.png"

    png_prompt = f"Enter output PNG filename [{default_png}]: "
    png_input = input(png_prompt).strip()
    output_png = png_input if png_input else default_png

    print(f"\nConverting '{input_pdf}' to '{output_png}'...")

    # Warn if a png file is going to be overwritten
    if not check_overwrite(output_png):
        print("Conversion cancelled.")
        return

    convert_pdf_to_png(input_pdf, output_png)


if __name__ == "__main__":
    main()
