import logging
import os
import requests
from osgeo import gdal

class TIFDownloader:

    def __init__(self, hdf_dir:str, tif_dir:str):
        self.hdf_dir = hdf_dir
        self.tif_dir = tif_dir
        self.sub_ds_index = None

    def download_raster(self, url, folder):
        """
        Downloads a raster file from the specified URL into the given folder.

        Parameters:
        - url (str): The URL from which to download the file.
        - folder (str): The local directory to save the downloaded file.

        Returns:
        - str: The local filepath of the downloaded file.

        Raises:
        - requests.exceptions.RequestException: If there is an error during the download.
        - ValueError: If the URL does not appear to reference a valid file (e.g., no filename in URL).
        """
        try:
            r = requests.get(url, verify=True, stream=True)
            r.raise_for_status()
            
            local_filename = os.path.basename(url)
            if not local_filename:
                raise ValueError(f"URL does not contain a valid filename: {url}")

            filepath = os.path.join(folder, local_filename)
            
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            logging.info(f"File downloaded successfully: {filepath}")
            return filepath
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download file: {url} due to {e}")
            raise


    def set_subdataset(self, subdataset):
        """Set the subdataset either by index or by its name string."""
        if isinstance(subdataset, int):
            self.sub_ds_index = subdataset
        elif isinstance(subdataset, str):
            self.sub_ds_index = subdataset
        else:
            raise ValueError("Subdataset must be an integer index or a string name.")

    def choose_subdataset(self, subDatasets):
        for index, (name, desc) in enumerate(subDatasets):
            print(f"{index}: {desc}")
        choice = input("Enter the index of the subdataset you want to use: ")
        try:
            choice = int(choice)
            if choice < 0 or choice >= len(subDatasets):
                raise ValueError("Invalid index.")
            self.sub_ds_index = choice
        except ValueError as e:
            print(f"Invalid choice: {e}")
            self.choose_subdataset(subDatasets) 

    def get_tif(self, hdf_filename):
        hdf_file = gdal.Open(hdf_filename)
        subDatasets = hdf_file.GetSubDatasets()
        if self.sub_ds_index is None:
            self.choose_subdataset(subDatasets)
        tif = gdal.Open(subDatasets[self.sub_ds_index][0])
        return tif

    def save_tif(self, hdf_filepath, tif):
        filepath = hdf_filepath.replace(self.hdf_dir, self.tif_dir).replace('.hdf', '.tif')
        trans_kwargs = {'dstSRS': 'EPSG:4326'}
        warp = gdal.Warp(filepath, tif, **trans_kwargs)
        warp = None
        return filepath

    def process_url(self, url):
        """
        Downloads and processes a file from the given URL. If the file is HDF, it's converted to TIF.
        
        Parameters:
        - url (str): The URL from which to download the file.
        
        Returns:
        - str: The filepath of the processed file.
        
        Raises:
        - ValueError: If the file has an invalid or unsupported extension.
        - FileNotFoundError: If the downloaded file is not found.
        """
        downloaded_filepath = self.download_raster(url)
        
        if not os.path.exists(downloaded_filepath):
            raise FileNotFoundError(f"Downloaded file not found at {downloaded_filepath}")
        
        file_ext = os.path.splitext(downloaded_filepath)[1].lower()
        
        if file_ext == ".tif":
            logging.info(f"Downloaded TIF file at {downloaded_filepath}")
            return downloaded_filepath
        elif file_ext == ".hdf":
            logging.info(f"Converting HDF file to TIF: {downloaded_filepath}")
            tif = self.convert_to_tif(downloaded_filepath)
            tif_filepath = self.save_tif(tif, downloaded_filepath.replace('.hdf', '.tif'))
            os.remove(downloaded_filepath)
            logging.info(f"Converted and saved TIF file at {tif_filepath}")
            return tif_filepath
        else:
            logging.error(f"Invalid file extension: {file_ext}")
            raise ValueError(f"Unsupported file extension: {file_ext}")
