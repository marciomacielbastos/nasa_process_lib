import rasterio
import rasterio.mask
from rasterio.merge import merge

class TifRasterProcessor:
    def __init__(self):
        pass

    def merge_rasters(self, filepath, tile_paths):
        granules = [rasterio.open(f) for f in tile_paths]
        mosaic, out_trans = merge(granules)
        out_meta = granules[0].meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans,
                         "crs": granules[0].crs})
        with rasterio.open(filepath, 'w', **out_meta) as dest:
            dest.write(mosaic)
        for granule in granules:
            granule.close()
        return mosaic

    def clip_raster(self, raster_path, aoi, clipped_path):
        with rasterio.open(raster_path, 'r') as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes=aoi.geometry, crop=True)
            out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        with rasterio.open(clipped_path, 'w', **out_meta) as dest:
            dest.write(out_image)
        return out_image
