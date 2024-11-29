import os
import random

template = {
    "modern1.pptx": {"length": 56, "p": 2, "s": 3, "m": 5, "b": 4},
    "modern2.pptx": {"length": 56, "p": 3, "s": 4, "m": 5, "b": 4},
    "modern3.pptx": {"length": 56, "p": 1, "s": 2, "m": 3, "b": 4},
    "modern4.pptx": {"length": 56, "p": 1, "s": 2, "m": 4, "b": 3},
    "color1.pptx": {"length": 56, "p": 2, "s": 3, "m": 4, "b": 5},
}

def getList(relative_folder_path):
    folder_path = os.path.abspath(relative_folder_path)
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except FileNotFoundError:
        print(f"The folder {relative_folder_path} does not exist.")
        return None

def PickPPT(style):
    base_path = os.getcwd()  # Get the current working directory
    if style == "0":
        folderpath = os.path.join(base_path, "PPT Templates", "Colors")
    elif style == "1":
        folderpath = os.path.join(base_path, "PPT Templates", "Modern")
    elif style == "2":
        folderpath = os.path.join(base_path, "PPT Templates", "Space")
    
    folderList = getList(folderpath)
    if not folderList:
        raise FileNotFoundError(f"Folder {folderpath} not found or is empty.")
    
    ppt = folderList[random.randrange(0, len(folderList))]
    return (os.path.join(folderpath, ppt), template[ppt])
