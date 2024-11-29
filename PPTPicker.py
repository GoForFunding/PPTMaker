import random 
import os 


template={
    
    "modern1.pptx":{"length":56,"p":2,"s":3,"m":5,"b":4} ,
    "modern2.pptx":{"length":56,"p":3,"s":4,"m":5,"b":4},
    "modern3.pptx":{"length":56,"p":1,"s":2,"m":3,"b":4},
    "modern4.pptx":{"length":56,"p":1,"s":2,"m":4,"b":3},
    "color1.pptx":{"length":56,"p":2,"s":3,"m":4,"b":5}
}

folderpath=""
def getList(relative_folder_path):
    folder_path = os.path.abspath(relative_folder_path)
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files 
    except FileNotFoundError:
        print(f"The folder {relative_folder_path} does not exist.")
def PickPPT(style):
    if style =="0":
        folderpath="PPT Templates\Colors"
    elif style=="1":
        folderpath="PPT Templates\Modern"
    elif style=="2":
        folderpath="PPT Templates\Space"
    folderList=getList(folderpath)
    ppt=folderList[random.randrange(0,len(folderList))]
    return (f"{folderpath}\{ppt}",template[ppt])
