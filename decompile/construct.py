#need install requests
import platform, requests, re, os, glob, zipfile

apktool_github = "https://github.com/iBotPeaches/Apktool"
apktool_bat = "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat"
apktool_shell = "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool"
bytecode_github = "https://github.com/Konloch/bytecode-viewer"
jadx_github = "https://github.com/skylot/jadx"

workspace = os.path.split(os.path.realpath(__file__))[0]
sysStr = platform.system()

tools_folder = workspace + "/Tools/"
apktool_folder = tools_folder + "apktool/"
bytecode_viewer_folder = tools_folder + "bytecode/"
jadx_folder = tools_folder + "jadx/"

def checkDirectory(dir):
    if not os.path.exists(dir):
        print("Create folder : " + dir)
        os.makedirs(dir)

def clearFolder(path):
    print("Clear folder : " + path)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def downloadFile(url, local_path):
    local_filename = url.split('/')[-1]
    path = local_path + local_filename
    r = requests.get(url, stream=True)
    size = 0
    total_size = int(r.headers.get('content-length', 0))
    if total_size >= 1024:
        chunk_size = 1024
        unit = "KB"
    else:
        chunk_size = 1
        unit = "Byte"
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                size += len(chunk)
                print(("\rtotal size:{0:.2f}" + unit + " [{2}] {1:.2f}%") \
                .format(float(total_size / chunk_size), float(size / total_size * 100), \
                '>' * int(size * 50 / total_size) + '=' * (50 - int(size * 50 / total_size))) , end='')
        print("\n")
    return path

def obtainApktool():
    print ("Obtain apktool")
    #检查目录
    checkDirectory(apktool_folder)
    #检查脚本文件
    if(sysStr =="Windows"):
        if not os.path.exists(apktool_folder + "apktool.bat"):
            print ("Obtain 'apktool.bat' file")
            downloadFile(apktool_bat, apktool_folder)
    elif(sysStr == "Linux"):
        if not os.path.exists(apktool_folder + "apktool"):
            print ("Obtain 'apktool' file")
            downloadFile(apktool_shell, apktool_folder)
    else:
        pass
    #获取最新版本tag
    print ("Obtain last version tag")
    new_ver_content = str(requests.get(apktool_github + "/releases/latest").content)
    res = r"(?<=/iBotPeaches/Apktool)/releases/download.+?\.jar"
    new_ver_path=re.search(res, new_ver_content).group(0)
    ver_file_path = apktool_folder + new_ver_path.split("/")[3] + ".ver"
    if not os.path.exists(ver_file_path):
        #是否存在旧文件,有则进行备份
        if os.path.exists(apktool_folder + "apktool.jar"):
            print ("Backup old version jar")
            #如果有旧的备份文件先删除
            if os.path.exists( apktool_folder + "apktool_backup.jar"):
                os.remove(apktool_folder + "apktool_backup.jar")
            os.rename(apktool_folder + "apktool.jar", apktool_folder + "apktool_backup.jar")
        print ("Obtain last version jar")
        current_path = downloadFile(apktool_github + new_ver_path, apktool_folder)
        os.rename(current_path, apktool_folder + "apktool.jar")
        #删除多余的tag
        for infile in glob.glob(os.path.join(apktool_folder, '*.ver')):
            os.remove(infile)
        #创建版本tag
        print ("Create tag.ver file")
        f = open(ver_file_path,'w')
        f.write(apktool_github + new_ver_path)
        f.close()

def obtainBytecodeViewer():
    print ("Obtain Bytecode Viewer")
    #检查目录
    checkDirectory(bytecode_viewer_folder)
    #获取最新版本tag
    print ("Obtain last version tag")
    new_ver_content = str(requests.get(bytecode_github + "/releases/latest").content)
    res = r"(?<=/Konloch/bytecode-viewer)/releases/download.+?\.jar"
    new_ver_path=re.search(res, new_ver_content).group(0)
    ver_file_path = bytecode_viewer_folder + new_ver_path.split("/")[3] + ".ver"
    if not os.path.exists(ver_file_path):
        #是否存在旧文件,有则进行备份
        if os.path.exists(bytecode_viewer_folder + "bytecode.jar"):
            print ("Backup old version jar")
            #如果有旧的备份文件先删除
            if os.path.exists( bytecode_viewer_folder + "bytecode_backup.jar"):
                os.remove(bytecode_viewer_folder + "bytecode_backup.jar")
            os.rename(bytecode_viewer_folder + "bytecode.jar", bytecode_viewer_folder + "bytecode_backup.jar")
        print ("Obtain last version jar")
        current_path = downloadFile(bytecode_github + new_ver_path, bytecode_viewer_folder)
        os.rename(current_path, bytecode_viewer_folder + "bytecode.jar")
        #删除多余的tag
        for infile in glob.glob(os.path.join(bytecode_viewer_folder, '*.ver')):
            os.remove(infile)
        #创建版本tag
        print ("Create tag.ver file")
        f = open(ver_file_path,'w')
        f.write(bytecode_viewer_folder + new_ver_path)
        f.close()

def obtainJadx():
    print("Obtain Jadx")
    #检查目录
    checkDirectory(jadx_folder)
    #获取最新版本tag
    print ("Obtain last version tag")
    new_ver_content = str(requests.get(jadx_github + "/releases/latest").content)
    res = r"(?<=/skylot/jadx)/releases/download.+?\.zip"
    new_ver_path=re.search(res, new_ver_content).group(0)
    ver_file_path = jadx_folder + new_ver_path.split("/")[3] + ".ver"
    if not os.path.exists(ver_file_path):
        #清除所有文件
        clearFolder(jadx_folder)
        print ("Obtain last version zip")
        current_path = downloadFile(jadx_github + new_ver_path, jadx_folder)
        fz = zipfile.ZipFile(current_path, 'r')
        for file in fz.namelist():
            fz.extract(file, jadx_folder)
        fz.close()
        os.remove(current_path)
        print ("Create tag.ver file")
        f = open(ver_file_path,'w')
        f.write(bytecode_viewer_folder + new_ver_path)
        f.close()


input("Please enter 'Enter' to start")
print("=============================")
print("Start construct tools")
print("Current workspace : " + workspace)
checkDirectory(tools_folder)
print("=============================")
obtainApktool()
print("=============================")
obtainBytecodeViewer()
print("=============================")
obtainJadx()
input("Please enter 'Enter' to finish")



