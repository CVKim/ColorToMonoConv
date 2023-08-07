
import numpy as np
import os
import cv2

import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory(title="폴더 선택"):
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=title)
    return folder_selected

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def convert_to_gray_scale(directory):
    SAVE_PATH = select_directory("Output Image Path")
    converted_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".bmp") and not file.endswith("_gray.bmp"):
                img_path = os.path.join(root, file)
                img = imread(img_path)

                if img is not None:
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    base = os.path.splitext(file)[0]
                    gray_img_path = os.path.join(SAVE_PATH, f"{base}_gray.bmp")

                    if os.path.exists(gray_img_path):
                        print(f'Grayscale image already exists: {gray_img_path}')
                        continue

                    imwrite(gray_img_path, gray_img)
                    converted_count += 1
                    print(f'Converted {img_path} to grayscale and saved as {gray_img_path}')
                else:
                    print(f'Invalid image file: {img_path}')
    
    root = tk.Tk()
    root.withdraw()
    print(f'Conver Processing End!!!, Count : {converted_count}')
    messagebox.showinfo("Convert End!!", f"총 {converted_count}개의 이미지가 grayscale로 변환되었습니다.")

def main():
    directory = select_directory("Input Image Path")
    
    if not os.path.exists(directory):  # Check if the directory exists
        print(f"지정된 경로 '{directory}'가 존재하지 않습니다. 경로를 확인 해주세요!!")
        return
    
    convert_to_gray_scale(directory)

if __name__ == "__main__":
    main()