import os
import gdown

def download_from_url(url, output_path):
    if not os.path.exists(output_path):
        try:
            path = output_path.split("/")
            folder_name = path[0]
            os.mkdir(folder_name)
            gdown.download(url, output_path, quiet=False, fuzzy=True)
            print("The Required files downloaded successfully ✅")
        except:
            print("Somthing went wrong, please try again❗")
    else:
        print("The Required files already exist ✅")