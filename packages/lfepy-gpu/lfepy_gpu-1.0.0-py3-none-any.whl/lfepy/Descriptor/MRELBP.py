import warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*cupyx.jit.rawkernel is experimental.*")
import cupy as cp
from lfepy.Helper import (NewRDLBP_Image, view_as_windows, get_mapping_info_ct, NILBP_Image_ct, RDLBP_Image_SmallestRadiusOnly)
from lfepy.Validator import validate_image, validate_kwargs, validate_mode


def MRELBP(image, **kwargs):
    """
    Compute the Median Robust Extended Local Binary Pattern (MRELBP) descriptors and histogram from an input image.

    Args:
        image (numpy.ndarray): Input image (preferably in NumPy array format).
        **kwargs (dict): Additional keyword arguments for customizing MRELBP extraction.
            mode (str): Mode for histogram computation. Options: 'nh' (normalized histogram) or 'h' (histogram). Default is 'nh'.

    Returns:
        tuple: A tuple containing:
            MRELBP_hist (cupy.ndarray): Histogram(s) of MRELBP descriptors.
            imgDesc (list of dicts): List of dictionaries where each dictionary contains the LBP descriptors for different radii. Each dictionary has:
                'fea': Features extracted for the specific radius, including:
                    'CImg': Processed image data after median filtering and LBP transformation.
                    'NILBPImage': Histogram of the No-Interpolation LBP image.
                    'RDLBPImage': Histogram of the Refined Descriptors LBP image.

    Raises:
        TypeError: If `image` is not a valid `numpy.ndarray`.
        ValueError: If `mode` in `kwargs` is not a valid option.

    Example:
        >>> import matplotlib.pyplot as plt
        >>> from matplotlib.image import imread

        >>> image = imread("Path")
        >>> histogram, imgDesc = MRELBP(image, mode='nh')

        >>> plt.imshow(imgDesc[0]['fea']['NILBPImage'].get(), cmap='gray')
        >>> plt.axis('off')
        >>> plt.show()
        >>> plt.imshow(imgDesc[0]['fea']['RDLBPImage'].get(), cmap='gray')
        >>> plt.axis('off')
        >>> plt.show()

    References:
        L. Liu, S. Lao, P.W. Fieguth, Y. Guo, X. Wang, and M. Pietikäinen,
        Median robust extended local binary pattern for texture classification,
        IEEE Transactions on Image Processing,
        vol. 25, no. 3, pp. 1368-1381, 2016.
    """
    # Input data validation
    image = validate_image(image)
    options = validate_kwargs(**kwargs)
    options = validate_mode(options)

    imSize = image.shape[0]
    lbpRadiusSet = [2, 4, 6, 8]
    imgDesc = []

    for idxLbpRadius in range(4):
        lbpRadius = lbpRadiusSet[idxLbpRadius]

        if idxLbpRadius > 0:
            lbpRadiusPre = lbpRadiusSet[idxLbpRadius - 1]
        else:
            lbpRadiusPre = 0

        lbpPoints = 8
        lbpMethod = 'MELBPEightSch1'
        mapping = get_mapping_info_ct(lbpRadius, lbpPoints, lbpMethod)
        numLBPbins = mapping['num']

        # Extend the image with symmetric padding
        imgExt = cp.pad(image, pad_width=1, mode='symmetric')
        imgblks = view_as_windows(imgExt, (3, 3)).reshape(-1, 9)
        a = cp.median(imgblks, axis=1)
        b = a.reshape(image.shape)
        CImg = b[lbpRadius:-lbpRadius, lbpRadius:-lbpRadius].flatten()
        CImg -= CImg.mean()
        CImg[CImg >= 0] = 2
        CImg[CImg < 0] = 1

        if lbpRadius == 2:
            # Special processing for radius 2
            filWin = 3
            halfWin = (filWin - 1) // 2
            imgExt = cp.pad(image, pad_width=halfWin, mode='symmetric')
            imgblks = view_as_windows(imgExt, (filWin, filWin)).reshape(-1, filWin ** 2)
            imgMedian = cp.median(imgblks, axis=1).reshape(image.shape)
            NILBPImage = NILBP_Image_ct(imgMedian, lbpPoints, mapping, 'image', lbpRadius)
            histNI = cp.histogram(NILBPImage, bins=cp.arange(numLBPbins + 1))[0]
            imgCurr = cp.reshape(imgMedian, image.shape)
            RDLBPImage = RDLBP_Image_SmallestRadiusOnly(b, imgCurr, lbpRadius, lbpPoints, mapping, 'image')
            histRD = cp.histogram(RDLBPImage, bins=cp.arange(numLBPbins + 1))[0]
        else:
            # General processing for other radii
            if lbpRadius % 2 == 0:
                filWin = lbpRadius + 1
            else:
                filWin = lbpRadius
            halfWin = (filWin - 1) // 2
            imgExt = cp.pad(image, pad_width=halfWin, mode='symmetric')
            imgblks = view_as_windows(imgExt, (filWin, filWin)).reshape(-1, filWin ** 2)
            imgMedian = cp.median(imgblks, axis=1).reshape(image.shape)
            imgCurr = cp.reshape(imgMedian, image.shape)
            NILBPImage = NILBP_Image_ct(imgCurr, lbpPoints, mapping, 'image', lbpRadius)
            histNI = cp.histogram(NILBPImage, bins=cp.arange(numLBPbins + 1))[0]

            if lbpRadiusPre % 2 == 0:
                filWin = lbpRadiusPre + 1
            else:
                filWin = lbpRadiusPre
            halfWin = (filWin - 1) // 2
            imgExt = cp.pad(image, pad_width=halfWin, mode='symmetric')
            imgblks = view_as_windows(imgExt, (filWin, filWin)).reshape(-1, filWin ** 2)
            imgMedian = cp.median(imgblks, axis=1).reshape(image.shape)
            imgPre = imgMedian
            imgCurr = cp.reshape(imgMedian, image.shape)
            RDLBPImage = NewRDLBP_Image(imgCurr, imgPre, lbpRadius, lbpRadiusPre, lbpPoints, mapping, 'image')
            histRD = cp.histogram(RDLBPImage, bins=cp.arange(numLBPbins + 1))[0]

        imgDesc.append({
            'fea': {
                'CImg': CImg.reshape((imSize - 4 * idxLbpRadius) - 4, -1),
                'NILBPImage': NILBPImage.reshape((imSize - 4 * idxLbpRadius) - 4, -1),
                'RDLBPImage': RDLBPImage.reshape((imSize - 4 * idxLbpRadius) - 4, -1)
            }
        })

    options['mrelbpHist'] = 1
    options['binVec'] = 800
    options['numLBPbins'] = numLBPbins

    # Compute MRELBP histogram
    MRELBP_hist = []
    for i in range(4):
        Joint_CINIRD = cp.zeros((options['numLBPbins'], options['numLBPbins'], 2), dtype=cp.float32)
        # Flatten the arrays and move them to GPU
        CImg = cp.array(imgDesc[i]['fea']['CImg'], dtype=cp.int32).flatten()
        NILBPImage = cp.array(imgDesc[i]['fea']['NILBPImage'], dtype=cp.int32).flatten()
        RDLBPImage = cp.array(imgDesc[i]['fea']['RDLBPImage'], dtype=cp.int32).flatten()
        indices = cp.stack((NILBPImage, RDLBPImage, CImg - 1), axis=-1)
        cp.add.at(Joint_CINIRD, (indices[:, 0], indices[:, 1], indices[:, 2]), 1)
        # Flatten the result for concatenation
        Joint_CINIRD = Joint_CINIRD.flatten()
        # Append the histogram to the MRELBP_hist array
        MRELBP_hist = cp.hstack((MRELBP_hist, Joint_CINIRD))

    if 'mode' in options and options['mode'] == 'nh':
        MRELBP_hist = MRELBP_hist / cp.sum(MRELBP_hist)

    return MRELBP_hist, imgDesc