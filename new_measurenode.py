# Import essential libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import math
import imutils
from pymongo import MongoClient
from datetime import datetime

# Initialize the database and YOLOv8 model for object segmentation
CONNECTION_STRING = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/'
client = MongoClient(CONNECTION_STRING)
Database = client['Dimension']
Input_Collection = Database['Preprocessed_Image']
Collection = Database['Bolt_Dimension']
mm_pixel = ((78/3088)+(53/2064))/2
model = YOLO("best.pt")
datasets_names = ""
print('!---- Initialized ----!')

# Receive the object(Ex. Thread, Head) and draw the bounding box line onto the image
def drawlines(img, object):
    # Check if there is data in the "object" parameter to prevent error
    if len(object) == 0:
        return img
    # Apply different color for parts in the bolt
    # Red for Head, Green for Grid, and Blue for Thread
    if object[4] == 'Head':
        c = (255, 0, 0)
    elif object[4] == 'Space':
        c = (0, 255, 0)
    elif object[4] == 'Thread':
        c = (0, 0, 255)

    x, y, w, h = object[:4]
    img = cv2.line(img, (round(x+w/2),round(y+h/2)), (round(x+w/2),round(y-h/2)), color=c, thickness = 5)
    img = cv2.line(img, (round(x+w/2),round(y+h/2)), (round(x-w/2),round(y+h/2)), color=c, thickness = 5) 
    img = cv2.line(img, (round(x-w/2),round(y-h/2)), (round(x+w/2),round(y-h/2)), color=c, thickness = 5) 
    img = cv2.line(img, (round(x-w/2),round(y-h/2)), (round(x-w/2),round(y+h/2)), color=c, thickness = 5) 
    return img

# Receive the object(Ex. Thread, Head) and mark corners of each object onto the image
def drawcorners(img, object):
    # Check if there is data in the "object" parameter to prevent error
    if len(object) == 0:
        return img
    x, y, w, h = object[:4]
    img = cv2.circle(img, (round(x+w/2),round(y+h/2)), radius=10, color=(96, 59, 42), thickness=-1)
    img = cv2.circle(img, (round(x-w/2),round(y+h/2)), radius=10, color=(96, 59, 42), thickness=-1)
    img = cv2.circle(img, (round(x+w/2),round(y-h/2)), radius=10, color=(96, 59, 42), thickness=-1)
    img = cv2.circle(img, (round(x-w/2),round(y-h/2)), radius=10, color=(96, 59, 42), thickness=-1)
    return img

# After the YOLOv8 segmentation model differentiate between the Head and the Thread,
# This function calculates the orientation in terms of angle and the slope of the bolt
# It returns the degree and the slope of the bolt, which will be further used to rotate the image
def findslope(H, T):
    # Slope determining
    slope = (T[1] - H[1]) / (T[0] - H[0])
    # Angle(In degree) determining
    degree = math.atan((T[1] - H[1]) / (T[0] - H[0]))*(180/math.pi)
    return degree, slope

# This function returns the four corners of the bolt as well as
# the width and the height of that the bolt
def findcorners(A, B):
    # Check if there is data in the "object" parameter to prevent error
    if len(A) == 0 and len(B) == 0:
        return 0, 0, 0
    x = [round(A[0]-A[2]/2), round(A[0]+A[2]/2), round(B[0]-B[2]/2), round(B[0]+B[2]/2)]
    y = [round(A[1]-A[3]/2), round(A[1]+A[3]/2), round(B[1]-B[3]/2), round(B[1]+B[3]/2)]
    p = [[min(x), min(y)], [max(x), min(y)], [min(x), max(y)], [max(x), max(y)]]
    delta_x = max(x)-min(x)
    delta_y = max(y)-min(y)
    return p, delta_x, delta_y

# The function elim_white_space eliminates the whitespaces that might be encountered between the bounding boxes and the object
# The function also takes the parameters height and width ratio, which are used to calculate the eliminated region
# It eliminates whitespaces from four sides of the image, including [left, right, top, bottom] respectively
def elim_white_space(img, object, height_ratio, width_ratio):
    corns = []
    if len(object) == 0:
        return corns
    sides = [round(object[0]-object[2]/2), round(object[0]+object[2]/2), round(object[1]-object[3]/2), round(object[1]+object[3]/2)]
    # sides = [left, right, top, bottom]
    Object_img = img

    #From the Top
    loop_break = False
    for row in range(sides[2], sides[3], 1):
        count = 0
        for col in range(sides[0], sides[1], 1):
            if (Object_img[row, col, 0] == 0 and Object_img[row, col, 1] == 0 and Object_img[row, col, 2] == 0):
                count += 1
                if count == round(round(object[2])*(height_ratio)):
                    Object_T = row
                    loop_break = True
                    break
        if loop_break:
            break

    #From the bottom
    loop_break = False
    for row in range(sides[3], sides[2], -1):
        count = 0
        for col in range(sides[0], sides[1], 1):
            if (Object_img[row, col, 0] == 0 and Object_img[row, col, 1] == 0 and Object_img[row, col, 2] == 0):
                count += 1
                if count == round(round(object[2])*(height_ratio)):
                    Object_B = row
                    loop_break = True
                    break
        if loop_break:
            break

    #From the Left
    loop_break = False
    for col in range(sides[0], sides[1], 1):
        count = 0
        for row in range(sides[2], sides[3], 1):
            if (Object_img[row, col, 0] == 0 and Object_img[row, col, 1] == 0 and Object_img[row, col, 2] == 0):
                count += 1
                if count == round(round(object[3])*(width_ratio)):
                    Object_L = col
                    loop_break = True
                    break
        if loop_break:
            break

    #From the Right
    loop_break = False
    for col in range(sides[1], sides[0], -1):
        count = 0
        for row in range(sides[2], sides[3], 1):
            if (Object_img[row, col, 0] == 0 and Object_img[row, col, 1] == 0 and Object_img[row, col, 2] == 0):
                count += 1
                if count == round(round(object[3])*(width_ratio)):
                    Object_R = col
                    loop_break = True
                    break
        if loop_break:
            break

    new_bounding_box = [Object_L + (Object_R - Object_L)/2, Object_T + (Object_B - Object_T)/2, Object_R - Object_L, Object_B - Object_T, object[4]]
    return img, new_bounding_box

# In instances where initial YOLOv8 detection was insufficient, bounding boxes were extended to cover the relevant areas of the object
def find_black_space(img, H, T):
    # The process iterate through the left and the right side of the bolt, finding the black area that is not covered by
    # the bounding boxes and cover that area
    offset = 0
    loop_count = 0
    for i in range(round(T[0]+T[2]/2), img.shape[1], 1): 
        count = 0
        for j in range(round(T[1]-T[3]/2), round(T[1]+T[3]/2), 1):
            if (img[j, i, 0] == 0 and img[j, i, 1] == 0 and img[j, i, 2] == 0):
                count += 1
        if count == 0:
            offset = loop_count
            break
        loop_count += 1
    Left_bound = T[0] - T[2]/2
    Right_bound = T[0] + T[2]/2 + offset
    Horizontal_Diff = Right_bound - Left_bound
    T = [(Left_bound + Horizontal_Diff/2), T[1], Horizontal_Diff, T[3], T[4]]
    return img, H, T

# This function optimize the length so that the length of the parts are reasonable
def optimize_length(H, S, T):
    if len(S) == 0:
        Left_Thread_Bound = H[0] + H[2]/2
        Right_Thread_Bound = T[0] + T[2]/2
        Thread_Diff = Right_Thread_Bound - Left_Thread_Bound
        T = [Left_Thread_Bound + Thread_Diff/2, T[1], Thread_Diff, T[3], T[4]]
    else:
        Left_Space_Bound = H[0] + H[2]/2
        Right_Space_Bound = T[0] - T[2]/2
        Space_Diff = Right_Space_Bound - Left_Space_Bound
        S = [Left_Space_Bound + Space_Diff/2, S[1], Space_Diff, S[3], S[4]]
    return H, S, T

# the maina function for image processing that calls other functions
def process_image(Display=False, Print=False, Publish=False, Draw=False, Label=False, path = None):
    # Load the image
    image = cv2.imread('processed.jpg')
    # Apply YOLOv8 segmentation model with confident level = 0.7
    results = model.predict('processed.jpg', conf=0.7, show=False)[0]

    Head = []
    Space = []
    Thread = []

    for i, obj in enumerate(results.boxes):
        x,y,w,h = obj.xywhn.cpu().numpy()[0]
        object_class = results.boxes.cls
        if object_class[i] == 0:
            Head = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Head']
        elif object_class[i] == 1:
            Space = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Space']
        elif object_class[i] == 2:
            Thread = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Thread']

    # Find the corners of the bolt
    corners, dx, dy = findcorners(Head, Thread)

    if corners == 0 and dx == 0 and dy == 0:
        pass
    else:
        # Crop the bolt image and move the image into the center
        cropimage = image[corners[0][1]:corners[3][1], corners[0][0]:corners[3][0]]
        image = np.ones((2064, 3088, 3), dtype=np.uint8) * 255
        image[math.ceil((2064-dy)/2):math.ceil(2064-(2064-dy)/2), math.ceil((3088-dx)/2):math.ceil(3088-(3088-dx)/2)] = cropimage

        # Find the angle of the bolt relative to the horizontal axis
        deg, sl = findslope(Head, Thread)
        # Rotate the image so that the bolt is parallel with the horizontal axis
        rot = imutils.rotate(image, angle=deg)
        if Head[0] > Thread[0]:
            rot = imutils.rotate(rot, angle=180)
        cv2.imwrite("rotated.jpg", rot)

        image = cv2.imread("rotated.jpg")
        # Apply YOLOv8 model on the rotated image
        results = model.predict("rotated.jpg", conf=0.75, show=False)[0]

        for i, obj in enumerate(results.boxes):
            x,y,w,h = obj.xywhn.cpu().numpy()[0]
            object_class = results.boxes.cls
            if object_class[i] == 0:
                Head = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Head']
            elif object_class[i] == 1:
                Space = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Space']
            elif object_class[i] == 2:
                Thread = [x*image.shape[1], y*image.shape[0], w*image.shape[1], h*image.shape[0], 'Thread']

        # Eliminate white space (The explaination of the process: Line 78)
        image, Head = elim_white_space(image, Head, 1/8, 1/8)
        image, Thread = elim_white_space(image, Thread, 1/400, 1/50)
        if len(Space) != 0:
            image, Space = elim_white_space(image, Space, 1/40, 1/40)

        # Find black space (The explanation of the process: 148)
        image, Head, Thread = find_black_space(image, Head, Thread)
        Head, Space, Thread = optimize_length(Head, Space, Thread)

        # Remove the corners of the image, resulting in better visualization of the bolt
        white_bg_image = np.full((image.shape[0], image.shape[1], 3), (255, 255, 255), dtype=np.uint8)
        for Object in [Head, Space, Thread]:
            if len(Object) != 0:
                white_bg_image[round(Object[1]-Object[3]/2):round(Object[1]+Object[3]/2),round(Object[0]-Object[2]/2):round(Object[0]+Object[2]/2)] = image[round(Object[1]-Object[3]/2):round(Object[1]+Object[3]/2), round(Object[0]-Object[2]/2):round(Object[0]+Object[2]/2)]
            else:
                pass
        image = white_bg_image

        # Calculation of the parameter including M_Size, Thread_Length, Thread_Diameter, Head_Thickness, Thread_Diameter, and Grid Length
        if len(Space) == 0:
            Space = [0, 0, 0, 0, 'Space']
            Space_Length = 0
        else:
            Space_Length = round((Space[2]*mm_pixel),2)

        if Space_Length <= 0:
            Space_Length = 0

        if round(Thread[3]*mm_pixel+0.21, 2) >= 2.3 and round(Thread[3]*mm_pixel+0.21, 2) <= 2.68:
            M_Size = 2.5
        else:
            M_Size = round(Thread[3]*mm_pixel+0.21)

        Thread_Length = round((Thread[2]*mm_pixel),2)
        Head_Thickness = round((Head[2]*mm_pixel),2)
        Head_Diameter = round((Head[3]*mm_pixel),2)
        Thread_Diameter = round((Thread[3]*mm_pixel + 0.06),2)

        # Print the value out in the terminal
        if Print:
            print('This is M'+str(M_Size)+' bolt.')
            print('Thread length = '+ str(Thread_Length)+' mm')
            print('Head Thickness = '+ str(Head_Thickness)+' mm')
            print('Head diameter = '+ str(Head_Diameter)+' mm')
            print('Grid length = '+ str(Space_Length)+' mm')

        # Send the value to the database for further use
        if Publish:
            count = Collection.count_documents({})
            data = {
            '_id': count+1,
            'M_Size': M_Size,
            'Head_Length' : Head_Thickness, 
            'Thread_Length' : Thread_Length, 
            'Head_Diameter' : Head_Diameter, 
            'Thread_Diameter' : Thread_Diameter, 
            'Space_Length' : Space_Length,
            'Timestamp' : datetime.utcnow()
            }
            Collection.insert_one(data)

        # Label the image with the lengths measured
        if Label:
            image = cv2.putText(image, 'M'+str(M_Size)+' bolt.', (800, 300), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA) 
            image = cv2.putText(image, 'Thread Diameter = '+ str(round((Thread[3]*mm_pixel)+0.21,2))+' mm', (800, 400), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA)
            image = cv2.putText(image, 'Bolt Length = '+str(round((Head[2] + Thread[2] + Space[2])*mm_pixel, 2))+' mm', (800, 500), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA) 
            image = cv2.putText(image, 'Thread length = '+ str(Thread_Length)+' mm', (800, 1550), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA) 
            image = cv2.putText(image, 'Head Thickness = '+ str(Head_Thickness)+' mm', (800, 1650), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA) 
            image = cv2.putText(image, 'Head diameter = '+ str(Head_Diameter)+' mm', (800, 1750), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA) 
            image = cv2.putText(image, 'Grid length = '+ str(Space_Length)+' mm', (800, 1850), cv2.FONT_HERSHEY_SIMPLEX , 3, (96, 59, 42), 6, cv2.LINE_AA)
        
        # Draw the bounding boxes, and the corners of the segmentations onto the image
        if Draw:
            Obj = [Space, Head, Thread]
            for components in Obj:
                image = drawcorners(image, components)
                image = drawlines(image, components)

        # Display the image using matplotlib.pyplot
        if Display:
            plt.imshow(image)
            plt.show()

        # Save the file to the device
        if path is not None:
            cv2.imwrite(path, image)


# Main part of the code
doc_count = Input_Collection.count_documents({})
while True:
    current_count = Input_Collection.count_documents({})
    # Check if there is new data appear in the Collection
    if current_count != doc_count:
        doc_cursor = Input_Collection.find()
        img_binary = doc_cursor[doc_count].get('img_binary')
        if img_binary:
            # Retrieve the image from the new data (Decoding image)
            image_array = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite('processed.jpg', image_array)
            # Process decoded image and send it to database
            process_image(Publish=True)
    else:
        pass
    doc_count = current_count
