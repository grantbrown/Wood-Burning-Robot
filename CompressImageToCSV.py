import numpy as np
from scipy import ndimage as img
import matplotlib.pyplot as plt

image = img.imread("./MomDad1.png")
outfilename = "./momdad1.csv"

def compress(im, pixels, invert = True):
    rw_int = im.shape[0]/pixels
    col_int = im.shape[1]/pixels
    outarr = np.zeros(shape = [rw_int, col_int],dtype = np.int32)
    for i in xrange(rw_int):
        for j in xrange(col_int):
            sub = im[(i*pixels):((i+1)*(pixels)),(j*pixels):((j+1)*pixels),0:3]
            #outarr[i, j] = np.sum(sub, 2) 
            maxval = np.prod(sub.shape)*256
            if invert:
                outarr[i,j] = (maxval - np.sum(sub))
            else:
                outarr[i,j] = np.sum(sub)
    return(outarr)

compressed = compress(image, 1, True)
#compressed = compressed.transpose()
compressed -= np.min(compressed)
compressed[0][0] = np.max(compressed)
#compressed_med = img.median_filter(compressed, 1)
plt.imshow(compressed, cmap = plt.cm.gray)
plt.show()


outfile = open(outfilename, "w")

for rw in compressed:
    outfile.write(",".join([str(int(x)) for x in rw]))
    outfile.write("\n")
