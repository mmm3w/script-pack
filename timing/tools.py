#相关工具
from requests import get
from os import path, makedirs, rename
from time import time, localtime, asctime


#########################################################################
def removeSpecialSymbol(str):
    return str.replace(" ", "").replace("\n", "").replace("\r", "")

def mergeStrList(list):
    return removeSpecialSymbol(str(''.join(list)))

def timef(t):
    if t == 23:
        return '00'
    else:
        return str(t + 1).zfill(2)

#########################################################################

numberContrastTable = {'0':'〇', '1':'一', '2':'二', '3':'三', '4':'四', '5':'五', '6':'六', '7':'七', '8':'八', '9':'九'}

def checkDirectory(dir):
    if not path.exists(dir):
        print("Create folder : " + dir)
        makedirs(dir)

def playLog(logFile, tag, content):
    logStr = '{0}\t|\t{1}\t|\t{2}\n'.format(tag, asctime(localtime(time())), content)
    file = open(logFile, 'a+', encoding='utf-8')
    file.write(logStr)
    file.close()

def downloadFile(download_url, local_path):
    local_filename = download_url.split('/')[-1]
    wait_path = local_path + "waiting_" + local_filename
    save_path = local_path + local_filename

    if path.exists(save_path):
        print('[Skip]{} already exists.'.format(save_path))
        return save_path

    try:
        r = get(download_url, stream=True)
    except:
        return save_path
        
    size = 0
    total_size = int(r.headers.get('content-length', 0))
    if total_size >= 1024:
        chunk_size = 1024
        unit = "KB"
    else:
        chunk_size = 1
        unit = "Byte"
    print("Download File : " + download_url)
    print("Total size : {0:.2f}{1}".format(float(total_size / chunk_size), unit))

    if path.exists(wait_path):
        if total_size == path.getsize(wait_path):
            rename(wait_path, save_path)
            print('[Skip]{} check over.'.format(save_path))
            return save_path

    with open(wait_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                size += len(chunk)
                print(("\rDownloading [{1}] {0:.2f}%") \
                .format( float(size / total_size * 100), \
                '>' * int(size * 50 / total_size) + '=' * (50 - int(size * 50 / total_size))) , end='')
    
    if total_size == path.getsize(wait_path):
            rename(wait_path, save_path)
    print()
    return save_path