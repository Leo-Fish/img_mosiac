from PIL import Image
import numpy as np
from random import randint

#check if the address is valid
def address_check(address):
    try:
        img=Image.open(address)
    except FileNotFoundError:
        print('please enter a valid address')
        address=input('please enter the location of the image you want to process\n')
        img=address_check(address)
    return img

# check if the size is valid
def size_check(area,shape):
    if (area[0]<0 or area[0]>shape[0]):
        area[0]=0
    if (area[1]<=0 or area[1]>shape[0]):
        area[1]=shape[1]
    if (area[2]<0 or area[2]>shape[1]):
        area[2]=0
    if (area[3]<=0 or area[3]>shape[1]):
        area[3]=shape[0]
    for coordinate in area:
        yield coordinate
 
# check if the ratio is valid        
def ratio_check(compression_ratio):
    values = compression_ratio.split(',')
    if len(values) == 2:
        try:
            ratio = list(int(val) for val in values)
        except ValueError:
            print("Please enter valid integers separated by a comma.")
            ratio = [2, 2]  
    else:
        print("Using default ratio: 2*2")
        ratio = [2, 2]  
    return ratio

# check if the area is valid
def area_check(shape,area):
    values = area.split(',')
    if len(values) == 4:
        try:
            area = list(int(val) for val in values)
        except ValueError:
            print("Please enter valid integers separated by a comma.")
            area = [0, shape[1], 0, shape[0]]  
    else:
        print("Using default area: whole image")
        area = [0, shape[1], 0, shape[0]] 
    return area

# basic mosaic 
def mosaic(img,compression_ratio=[2,2],area=[0,0,0,0]):
    shape=img.shape
    area=size_check(area,shape)
    horrizontal_start, horrizontal_end,vertical_start, vertical_end=area
    vertical_start,vertical_end=abs(shape[0]-vertical_end),abs(shape[0]-vertical_start) #switched the y so that it performs like regular axis
    color=shape[2]
    vertical_ratio=compression_ratio[0]
    horrizontal_ratio=compression_ratio[1]
    for i in range(vertical_start,vertical_end-vertical_ratio,vertical_ratio):
        for j in range(horrizontal_start,horrizontal_end-horrizontal_ratio,horrizontal_ratio):
            cur_pixel=img[i][j]
            for x in range(vertical_ratio):
                for y in range(horrizontal_ratio):
                    img[i+x][j+y]=cur_pixel
    return img

#glass window 
def glass_window(img,compression_ratio=[2,2],area=[0,0,0,0]):
    shape=img.shape
    area=size_check(area,shape)
    horrizontal_start, horrizontal_end,vertical_start, vertical_end=area
    vertical_start,vertical_end=abs(shape[0]-vertical_end),abs(shape[0]-vertical_start)
    color=shape[2]
    vertical_ratio=compression_ratio[0]
    horrizontal_ratio=compression_ratio[1]
    for i in range(vertical_start,vertical_end-vertical_ratio):
        for j in range(horrizontal_start,horrizontal_end-horrizontal_ratio):
            index=randint(1,vertical_ratio)
            img[i][j]=img[i+index][j+index]
    return img

#average color sampling
def average_col_sampling(img,compression_ratio=[2,2],area=[0,0,0,0]):
    shape=img.shape
    area=size_check(area,shape)
    horrizontal_start, horrizontal_end,vertical_start, vertical_end=area
    vertical_start,vertical_end=abs(shape[0]-vertical_end),abs(shape[0]-vertical_start)
    color=shape[2]
    vertical_ratio=compression_ratio[0]
    horrizontal_ratio=compression_ratio[1]
    for i in range(vertical_start,vertical_end-vertical_ratio,vertical_ratio):
        for j in range(horrizontal_start,horrizontal_end-horrizontal_ratio,horrizontal_ratio):
            sum=np.zeros(color)
            for x in range(vertical_ratio):
                for y in range(horrizontal_ratio):
                    sum+=img[i+x][j+y]
            average=sum/(vertical_ratio*horrizontal_ratio)
            for x in range(vertical_ratio):
                for y in range(horrizontal_ratio):
                    img[i+x][j+y]=average
    return img

img_loc=input('please enter the location of the image you want to process\n')
img=address_check(img_loc) 
sav_loc=None
sav_loc=input('please enter the location you want to save the image. (If you don\'t want to save, just press enter)\n')

img=np.array(img)
mosaic_type=input('please enter the way(in number form) you want to process the image\n1.mosaic\n2.glass window\n3.average color sampling\n')
compression_ratio=input('please enter the compression ratio seperated by comma (default value will be 2,2)\n')
compression_ratio=ratio_check(compression_ratio)
area=input('please enter the area you want to mosaic(default value will be the 0,1920,0,1080 for 1080p)\n')
area=area_check(img.shape,area)
match mosaic_type:
    # mosaic
    case '1':
        img=mosaic(img,compression_ratio,area)
    #glass window
    case '2':
        img=glass_window(img,compression_ratio,area)
    #average color sampling
    case '3':
        img=average_col_sampling(img,compression_ratio,area)
        
img=Image.fromarray(img)
img.show()

if sav_loc:
    img.save(sav_loc)

