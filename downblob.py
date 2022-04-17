import os
import yaml
from azure.storage.blob import ContainerClient

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader= yaml.FullLoader)

def download_files(direct_folder, connection_string, container_name):
    #define a container client; knows container and credentials
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    download_file_path = os.path.join(direct_folder)

    print("Donwloading blob to ", download_file_path)
    blob_client = container_client.get_blob_client(container=container_name)

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
        print("Downloaded from blob storage successfully! Now party!")    

config = load_config()
download_files(config["direct_folder"], config["azure_storage_connnectionstring"], config['pictures_container_name'])