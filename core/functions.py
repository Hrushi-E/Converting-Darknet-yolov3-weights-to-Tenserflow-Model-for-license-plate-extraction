import os
import cv2
import random
import numpy as np
import tensorflow as tf
import pytesseract
from core.utils import read_class_names
from core.config import cfg

# function to count objects, can return total classes or count per class
def count_objects(data, by_class = False, allowed_classes = list(read_class_names(cfg.YOLO.CLASSES).values())):
    boxes, scores, classes, num_objects = data

    #create dictionary to hold count of objects
    counts = dict()

    # if by_class = True then count objects per class
    if by_class:
        class_names = read_class_names(cfg.YOLO.CLASSES)

        # loop through total number of objects found
        for i in range(num_objects):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            if class_name in allowed_classes:
                counts[class_name] = counts.get(class_name, 0) + 1
            else:
                continue

    # else count total objects found
    else:
        counts['total object'] = num_objects
    
    return counts

# function for cropping each detection and saving as new image
def crop_objects(img, data, path, allowed_classes):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)
    #create dictionary to hold count of objects for image name
    counts = dict()
    for i in range(num_objects):
        # get count of class for part of image name
        class_index = int(classes[i])
        class_name = class_names[class_index]
        if class_name in allowed_classes:
            counts[class_name] = counts.get(class_name, 0) + 1
            # get box coords
            xmin, ymin, xmax, ymax = boxes[i]
            # crop detection from image (take an additional 5 pixels around all edges)
            cropped_img = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5]
            # construct image name and join it to path for saving crop properly
            img_name = class_name + '_' + str(counts[class_name]) + '.png'
            img_path = os.path.join(path, img_name )
            # save image
            cv2.imwrite(img_path, cropped_img)
        else:
            continue

            
# function for cropping each detection and saving as new image
def crop_objects(img, data, path, allowed_classes):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)
    #create dictionary to hold count of objects for image name
    counts = dict()
    # mine
    for i in range(num_objects):
        p=[];lp=[];h=[];nh=[];mc=[];mcn=[];pwoh=[];temp=0
        # get count of class for part of image name
        class_index = int(classes[i])
        class_name = class_names[class_index]
        xmin, ymin, xmax, ymax = boxes[i]
        if class_name =='Person':
            p.append([xmin, ymin, xmax, ymax])
        elif class_name =='Helmet':
            h.append([xmin, ymin, xmax, ymax])
        elif class_name=='Vehicle_reg_number':
            lp.append([xmin, ymin, xmax, ymax])
        m=len(p)
        n=len(h)
        o=len(lp)
        e=len(nh)
        f=len(mc)
        for j in range(e):
            c0=p[j][0];d0=p[j][1];c1=p[j][2];d1=p[j][3];
            for k in range(m):
                x0==nh[k][0]
                y0==nh[k][1]
                x1==nh[k][2]
                y1==nh[k][3]
                if (x0<c0 and y0<d1)and(x1>c1 and y1>d1):
                    pwoh.append([x0,y0,x1,y1])
                    break

        s=len(pwoh)
        for k in range(s):
            x0=pwoh[k][0]; y0=pwoh[k][1]; x1=pwoh[k][2]; y1=pwoh[k][3]; 
            for j in range(f):
                a0=lp[j][0]
                b0=lp[j][1]
                a1=lp[j][2]
                b1=lp[j][3]

                # If one rectangle is on left side of other
                if(x0 >= a1 or a0 >= x1):
                    continue
                # If one rectangle is above other
                if(y0 <= b1 or b0 <= y1):
                    continue
                else:
                    mcn.append([a0,b0,a1,b1])
 

        #detection of lp without helmet
        g=len(mcn)
        for k in range(g):
            x0=mcn[k][0];y0=mcnh[k][1];x1=mcn[k][2];y1=mcn[k][3];
            for j in range(o):
                a0=lp[j][0]
                b0=lp[j][1]
                a1=lp[j][2]
                b1=lp[j][3]
                if (a0<x0 and b0<y0) and (a1<x1 and b0<y1):
                    temp=1
                    xmin=a0;ymin=b0;xmax=a1;ymax=b1
                    # crop detection from image (take an additional 5 pixels around all edges)
                    cropped_img = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5]
                    # construct image name and join it to path for saving crop properly
                    img_name = class_name + '_' + str(counts[class_name]) + '.png'
                    img_path = os.path.join(path, img_name)
                    # save image
                    cv2.imwrite(img_path, cropped_img)

                    

# function to run general Tesseract OCR on any detections 
def ocr(img, data):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)
    for i in range(num_objects):
        # get class name for detection
        class_index = int(classes[i])
        class_name = class_names[class_index]
        # separate coordinates from box
        xmin, ymin, xmax, ymax = boxes[i]
        # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
        box = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5]
        # grayscale region within bounding box
        gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY)
        # threshold the image using Otsus method to preprocess for tesseract
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # perform a median blur to smooth image slightly
        blur = cv2.medianBlur(thresh, 3)
        # resize image to double the original size as tesseract does better with certain text size
        blur = cv2.resize(blur, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        # run tesseract and convert image text to string
        try:
            text = pytesseract.image_to_string(blur, config='--psm 11 --oem 3')
            print("Class: {}, Text Extracted: {}".format(class_name, text))
            with open('LicensePlate.txt', 'w') as f:
                f.write(text)
                f.write('\n')
                f.close()
        except: 
            text = None
