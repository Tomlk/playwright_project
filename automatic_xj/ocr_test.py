import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
img = cv2.imread('images/ocr3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
blur = cv2.GaussianBlur(threshold, (5,5), 0)
contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
count = 0
result=''
for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    if w > 10 and h > 10:
        roi = blur[y:y+h, x:x+w]
        cv2.imwrite(str(count)+'.jpg', roi)
        text = pytesseract.image_to_string(roi, lang='eng')
        # print(text)
        if text!='':
            result=text
            result = result.strip()
        count += 1
print(result)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#
#
# import pytesseract
# try:
#     from PIL import Image
# except ImportError:
#     import Image
#
# pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
# # 列出支持的语言
# print(pytesseract.get_languages(config=''))
#
# img=Image.open('images/ocr2.png')
# text=pytesseract.image_to_string(img, lang='chi_sim+eng')
# print(text)


# import pytesseract
# from PIL import Image
#
# image = Image.open('images/ocr1.png')
# text = pytesseract.image_to_string(image, lang=)
# print(text.replace(" ", ""))