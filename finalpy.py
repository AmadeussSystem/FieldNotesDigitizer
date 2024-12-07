import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os

def remove_ink_and_make_transparent(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)  
    

    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    

    image_rgba[:, :, 3] = mask  
    
    return image_rgba


def convert_pdf_to_images(pdf_path, output_folder):

    images = convert_from_path(pdf_path, 300)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    for idx, image in enumerate(images):

        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1]  
        
        transparent_image = remove_ink_and_make_transparent(open_cv_image)
    
        transparent_image_pil = Image.fromarray(transparent_image)

        output_image_path = os.path.join(output_folder, f'page_{idx + 1}.png')
        transparent_image_pil.save(output_image_path, 'PNG')
        print(f"Page {idx + 1} processed and saved as {output_image_path}")


if __name__ == "__main__":

    pdf_path = input("Enter the full path to the PDF file: ").strip()

    if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):

        output_folder = os.path.expanduser(f"~/{os.path.basename(pdf_path).split('.')[0]}_Converted")

        convert_pdf_to_images(pdf_path, output_folder)
        
        print("Conversion completed. All pages processed and saved.")
    else:
        print("Invalid PDF path provided. Please make sure the file exists and has a .pdf extension.")
