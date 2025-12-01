import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import find_peaks

# 1 - Importer image : 
# Ouverture de l'image
image2D = plt.imread("C:\\Users\\gauth\\OneDrive\\Documents\\Polytechnique\\Polytechnique automne 2025\\Techniques expérimentales et instrumentation\\Mandat 3\\Photo_calibration2\\500_filtre.jpeg")
        
# Conversion de l'image de RGBA à gris 
image2D = cv2.cvtColor(image2D, cv2.COLOR_RGBA2GRAY)
plt.imshow(image2D)
plt.show()

height, width = image2D.shape

x = np.zeros(width)
for i in range(width):
    x[i] = np.sum(image2D[:,i])


peaks, properties = find_peaks(x,prominence=0.5,width=5,distance = 5000)

plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.vlines(x=peaks, ymin=x[peaks] - properties["prominences"],
           ymax = x[peaks], color = "C1")
plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"],
           xmax=properties["right_ips"], color = "C1")
plt.show()

print("peaks :", peaks)
print("moitié largeur :", properties["widths"]/2)