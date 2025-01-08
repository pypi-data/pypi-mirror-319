import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda
# from skimage.data import cells3d
#
# im = cells3d()
# 0.29 0.26 0.26
img = r"E:\1_DATA\Rheenen\tvl_jr\3d stitching\raw4-deep\raw.tif"

masks = cellstitch_cuda(img, output_masks=True, verbose=True, seg_mode="nuclei_cells", n_jobs=-1)
