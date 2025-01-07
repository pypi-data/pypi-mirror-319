import sys
from paddleocr import PaddleOCR, draw_ocr
import time
from PIL import Image
import numpy as np

class CustomImageOpt():
  def __init__(self,path):
    self.origin_image_path=path
  
  def get_ocr_text_in_lines(self):
    if hasattr(self,'ocr')==False:
    # C:\Users\40211/.paddleocr/whl\cls\ch_ppocr_mobile_v2.0_cls_infer\ch_ppocr_mobile_v2.0_cls_infer.tar
      self.ocr=PaddleOCR(use_angle_cls=True, lang="ch")
      
    result = self.ocr.ocr(self.origin_image_path, cls=True)
    output=[]
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            output.append(line)
    output.sort(key=lambda x:x[0][0][0])
    lines=[one[1][0] for one in output]
  # result = result[0]
  # image = Image.open(img_path).convert('RGB')
  # boxes = [line[0] for line in result]
  # txts = [line[1][0] for line in result]
  # scores = [line[1][1] for line in result]
  # im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
  # im_show = Image.fromarray(im_show)
  # im_show.save('result.jpg')
    return lines

  
img_path=r'C:\Users\40211\Desktop\记录\新建文件夹\IMG_20210520_231022.jpg'
# image = Image.open(img_path).convert('RGB')
# print(image.size)
a=CustomImageOpt(img_path)
output=a.get_ocr_text_in_lines()
print("".join(output))