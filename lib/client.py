import earthaccess
from injector import Injector
import os

from nasa_tif_lib.container import ApiModule
from nasa_tif_lib.processors.tif_downloader import TIFDownloader
from nasa_tif_lib.processors.tif_processor import TifProcessor
from nasa_tif_lib.processors.url_grouper import UrlGrouper

class Client:
    def __init__(self, input_dir, output_dir) -> None:
        earthaccess.login(persist=True)
        self.injector = Injector([ApiModule(input_dir, output_dir)])

    def get_src_urls(self, source_list, polygon, time_interval):
        results = earthaccess.search_data(short_name=source_list,
                                          bounding_box=polygon,
                                          temporal=time_interval
        )
        return [granule.data_links()[0] for granule in results]
    
    def weekly_process(self, urls, output_dir, polygon):
        grouper = self.injector.get(UrlGrouper)
        downloader = self.injector.get(TIFDownloader)
        processor = self.injector.get(TifProcessor)
        grouped_urls = grouper.group_weekly_urls(urls=urls)
        for group in grouped_urls.items():
            files = []
            for url in group[1]:
                files.append(downloader.process_url(url))
            merged_path = os.path.join(output_dir, f"{group[0]}.tif")
            clipped_path = os.path.join(output_dir, f"clipped_{group[0]}.tif")
            processor.merge(merged_path, files)
            processor.clip(merged_path, polygon, clipped_path)
            os.remove(merged_path)
            
                
        
        
    

