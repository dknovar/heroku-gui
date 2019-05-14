from skimage.transform import rescale, resize, downscale_local_mean
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import os
import glob
from skimage import io, transform, morphology, exposure
from skimage.color import rgb2gray,gray2rgb,rgb2hsv, rgb2lab
from skimage.filters import threshold_otsu, threshold_local, sobel
from skimage.morphology import label, square, erosion, dilation, opening, closing, binary_closing, binary_dilation
from skimage.measure import label, regionprops, find_contours
from skimage.morphology import disk
from PIL import Image, ImageEnhance
from skimage.color import label2rgb
from sklearn import svm
from sklearn.metrics import accuracy_score
from skimage.feature import greycomatrix, greycoprops
from skimage import img_as_ubyte
from joblib import dump, load
import io
import urllib


def process(path):
    URL = 'https://earweb.herokuapp.com'+path
    with urllib.request.urlopen(URL) as url:
        f = io.BytesIO(url.read())
    im=Image.open(f)
    # Preprocessing
    brightness = 1.5
    enhancer = ImageEnhance.Brightness(im)
    bright = enhancer.enhance(brightness)
    contrast = 1.5
    enhancer = ImageEnhance.Contrast(bright)
    con = enhancer.enhance(contrast)
    #Resize
    width = 400
    height = 400
    dim = (height,width)
    imge =np.array(con)
    img_resize = resize(imge, (dim),anti_aliasing=True)
    #Grayscale
    imGray = rgb2gray(img_resize)
    # Eaktrasi Ciri
    #HSV
    H = []
    S = []
    V = []

    hsv_img = rgb2hsv(img_resize)
    hue, s, v = hsv_img[:, :, 0], hsv_img[:, :, 1], hsv_img[:, :, 2]

    # HSV Processing
    H=np.mean(hue)
    S=np.mean(s)
    V=np.mean(v)
    hsv=[H,S,V]

    #GLCM
    glcm = []
    image = img_as_ubyte(imGray)#Rubah ke int
    g = greycomatrix(image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256,normed=True, symmetric=True)
    c =(greycoprops(g, 'contrast'))
    d =(greycoprops(g, 'dissimilarity'))
    a =(greycoprops(g, 'ASM'))
    e =(greycoprops(g, 'energy'))
    h =(greycoprops(g, 'homogeneity'))
    co =(greycoprops(g, 'correlation'))
    #       

    for i in c[0]:
        glcm.append(i) #Nilai contrast 
    for j in d[0]:
        glcm.append(j) #Nilai dissimilarity
    for k in a[0]:
        glcm.append(k) #Nilai ASM
    for l in e[0]:
        glcm.append(l) #Nilai energy
    for m in h[0]:
        glcm.append(m) #Nilai homogeneity
    for n in co[0]:
        glcm.append(n) #Nilai correlation

    #Memasukan semua nilai ciri ke dalam array
    feature=[]
    ciri=[]
    for i in hsv:
        ciri.append(i)
    for j in glcm:
        ciri.append(j)

    #         print(ciri)
    feature.append(ciri)
    # Klasifikasi
    model = load('ModelTest5.joblib')
    # print(model)
    predicted_labels = model.predict(feature)
    proba=model.predict_proba(feature)

    return (con,imGray,hue,s,v,feature,predicted_labels,proba)