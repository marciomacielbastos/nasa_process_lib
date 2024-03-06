from injector import Module, singleton

from nasa_tif_lib.processors.tif_downloader import TIFDownloader
from nasa_tif_lib.processors.tif_processor import TifProcessor
from nasa_tif_lib.processors.url_grouper import UrlGrouper

class ApiModule(Module):
    def __init__(self, hdf_dir: str, tif_dir: str):
        self.hdf_dir = hdf_dir
        self.tif_dir = tif_dir

    def configure(self, binder):
        binder.bind(TIFDownloader, to=lambda: TIFDownloader(hdf_dir=self.hdf_dir, tif_dir=self.tif_dir), scope=singleton)
        binder.bind(TifProcessor, to=TifProcessor, scope=singleton)
        binder.bind(UrlGrouper, to=UrlGrouper, scope=singleton)