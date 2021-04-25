from __future__ import print_function, absolute_import, division
from math import floor, ceil
from skimage import img_as_ubyte
from skimage.measure import find_contours
from skimage.util import crop
from skimage.transform import resize
from skimage.filters import threshold_otsu, sobel, try_all_threshold, threshold_li, threshold_triangle

import matplotlib.pyplot as plt

SHIFT_PIXEL = 10 # shift image from right to left
# BINARY_THRESH = 30 # image binary thresh
LETTER_SIZE = (38, 38) # letter width, heigth

def split_letters(image, num_letters=6, debug=False):
    '''
    split full captcha image into `num_letters` lettersself.
    return list of letters binary image (0: white, 255: black)
    '''
    print(num_letters)
    #plt.imshow(image)
    #plt.show()

    # move left
    # left = crop(image, ((0, 0), (0, image.shape[1]-SHIFT_PIXEL)), copy=True)
    # image[:,:-SHIFT_PIXEL] = image[:,SHIFT_PIXEL:]
    # image[:,-SHIFT_PIXEL:] = left
    # binarization
    # fig, ax = try_all_threshold(image, figsize=(10, 8), verbose=False)
    # plt.show()  
    BINARY_THRESH = threshold_otsu(image) 
    # BINARY_THRESH = threshold_li(image) 
    # BINARY_THRESH = threshold_triangle(image) 
    binary = image > BINARY_THRESH
    # plt.imshow(binary)
    # plt.show()
    # find contours
    contours1 = find_contours(binary)
    # fig, ax = plt.subplots()
    # ax.imshow(image, cmap=plt.cm.gray)

    # for contour in contours1:
    #     ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    # plt.show()
    contours = [[
        [int(floor(min(contour[:, 1]))), int(floor(min(contour[:, 0])))], # top-left point
        [int(ceil(max(contour[:, 1]))), int(ceil(max(contour[:, 0])))]  # down-right point
      ] for contour in contours1]
    # plt.imshow(binary, interpolation='nearest', cmap=plt.cm.gray)
    # for [x_min, y_min], [x_max, y_max] in contours:
    #     plt.plot(
    #         [x_min, x_max, x_max, x_min, x_min],
    #         [y_min, y_min, y_max, y_max, y_min],
    #         linewidth=2)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    # keep letters order
    contours = sorted(contours, key=lambda contour: contour[0][0])
    # find letters box
    print(len(contours))
    letter_boxs = []
    le=num_letters
    for contour in contours:
        if len(letter_boxs) > 0 and contour[0][0] < letter_boxs[-1][1][0] - 10:
            # skip inner contour
            print(contour)
            continue
        # extract letter boxs by contour
        boxs = get_letter_boxs(binary, contour,le)
        le-=len(boxs)
        for box in boxs:
            letter_boxs.append(box)
    # check letter outer boxs number
    print(letter_boxs)
    # plt.imshow(binary, interpolation='nearest', cmap=plt.cm.gray)
    # for [x_min, y_min], [x_max, y_max] in letter_boxs:
    #     plt.plot(
    #         [x_min, x_max, x_max, x_min, x_min],
    #         [y_min, y_min, y_max, y_max, y_min],
    #         linewidth=2)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    if len(letter_boxs) != num_letters:
        print('ERROR: number of letters is NOT valid', len(letter_boxs))
        # debug
        if debug:
            print(letter_boxs)
            plt.imshow(binary, interpolation='nearest', cmap=plt.cm.gray)
            for [x_min, y_min], [x_max, y_max] in letter_boxs:
                plt.plot(
                    [x_min, x_max, x_max, x_min, x_min],
                    [y_min, y_min, y_max, y_max, y_min],
                    linewidth=2)
            plt.xticks([])
            plt.yticks([])
            plt.show()
        return None

    # normalize size (40x40)
    letters = []
    for [x_min, y_min], [x_max, y_max] in letter_boxs:
        letter = resize(image[y_min:y_max, x_min:x_max], LETTER_SIZE)
        letter = img_as_ubyte(letter < 0.6)
        letters.append(letter)

    return letters

def get_letter_boxs(binary, contour,le):
    if(le==0):
        return []
    boxs = []
    w = contour[1][0] - contour[0][0] # width
    h = contour[1][1] - contour[0][1] # height
    if w < 10:
        # skip too small contour (noise)
        return boxs

    if (w < LETTER_SIZE[0] and w / h < 1.6) or le==1:
        boxs.append(contour)
    else:
        # split 2 letters if w is large
        t=min(int(round(w/LETTER_SIZE[0]))+1,le)
        p=int(round(w/t))
        print(t)
        print(p)
        sub_contours=[]
        topx = contour[0][1]
        botx = contour[1][1]
        prev1=contour[0][0]  
        for f in range(t):
            sub_contours.append([[prev1,topx],[prev1+p,botx]])
            prev1+=p

        # x_mean = contour[0][0] + int(round(w / 2))
        # sub_contours = [
        #     [contour[0], [x_mean, contour[1][1]]],
        #     [[x_mean, contour[0][1]], contour[1]]
        # ]
        for [x_min, y_min], [x_max, y_max] in sub_contours:
            # fit y_min, y_max
            y_min_val = min(binary[y_min + 1, x_min:x_max])
            y_max_val = min(binary[y_max - 1, x_min:x_max])
            while y_min_val or y_max_val:
                print([[x_min,y_min],[x_max,y_max]])
                if y_min_val:
                    y_min += 1
                    y_min_val = min(binary[y_min + 1, x_min:x_max])
                if y_max_val:
                    y_max -= 1
                    y_max_val = min(binary[y_max - 1, x_min:x_max])
            boxs.append([[x_min, y_min], [x_max, y_max]])

    return boxs
