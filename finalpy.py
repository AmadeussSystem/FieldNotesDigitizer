import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os

# Function to remove ink from background and make it transparent
def remove_ink_and_make_transparent(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to create a mask where the text is (black ink), background is white
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)  # Adjust the threshold for ink
    
    # Make the image have an alpha channel (RGBA)
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Set the background (white areas) to be fully transparent
    image_rgba[:, :, 3] = mask  # Use the mask to define where transparency should be
    
    return image_rgba

# Function to convert each PDF page to an image, process it, and save
def convert_pdf_to_images(pdf_path, output_folder):
    # Convert PDF to images (300 DPI for good quality)
    images = convert_from_path(pdf_path, 300)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each image and save as PNG with transparent background
    for idx, image in enumerate(images):
        # Convert PIL image to OpenCV format for processing
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1]  # Convert RGB to BGR
        
        # Remove ink and make the background transparent
        transparent_image = remove_ink_and_make_transparent(open_cv_image)
        
        # Convert back to PIL for saving as PNG
        transparent_image_pil = Image.fromarray(transparent_image)
        
        # Save the processed image with transparent background
        output_image_path = os.path.join(output_folder, f'page_{idx + 1}.png')
        transparent_image_pil.save(output_image_path, 'PNG')
        print(f"Page {idx + 1} processed and saved as {output_image_path}")


if __name__ == "__main__":
    # Ask user for the path to the PDF file
    pdf_path = input("Enter the full path to the PDF file: ").strip()
    
    # Validate the input path
    if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
        # Output folder where processed images will be saved
        output_folder = os.path.expanduser(f"~/{os.path.basename(pdf_path).split('.')[0]}_Converted")
        
        # Call the function to process the PDF
        convert_pdf_to_images(pdf_path, output_folder)
        
        print("Conversion completed. All pages processed and saved.")
    else:
        print("Invalid PDF path provided. Please make sure the file exists and has a .pdf extension.")
