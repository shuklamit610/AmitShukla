"""
QR Code Generator

This program accepts a URL from the user, generates a QR code,
saves it as an image, and displays the generated QR code.
"""

import qrcode
from PIL import Image


def generate_qr_code(url, filename="qr_code.png"):
    """
    Generate a QR code from the provided URL.

    Args:
        url (str): Website URL to encode in the QR code.
        filename (str): Name of the output image file.

    Returns:
        str: Name of the generated image file.
    """

    # Create the QR code object.
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    # Add the URL to the QR code.
    qr.add_data(url)

    # Generate the QR code.
    qr.make(fit=True)

    # Create a black-and-white QR code image.
    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    # Save the QR code as a PNG image.
    img.save(filename)

    return filename


def main():
    """Run the QR code generator."""

    print("================================")
    print("       QR Code Generator")
    print("================================")

    # Ask the user to enter a URL.
    url = input("Enter the URL: ").strip()

    # Check that the user entered a URL.
    if not url:
        print("Error: URL cannot be empty.")
        return

    # Generate the QR code.
    filename = generate_qr_code(url)

    print(f"QR code saved as: {filename}")

    # Open and display the generated QR code.
    image = Image.open(filename)
    image.show()


if __name__ == "__main__":
    main()