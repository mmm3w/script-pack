import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pixiv.download import downloadartworks
from pixiv.user import initsession

try:
    session, headers = initsession()
    if len(sys.argv) > 1:
        savedir = sys.argv[1]
        if len(savedir) == 0:
            savedir = os.path.split(os.path.realpath(__file__))[0]
    else:
        savedir = os.path.split(os.path.realpath(__file__))[0]
    while 1:
        id = ''.join(input("Input artwork id:").split())
        if len(id) == 0:
            break
        isoriginal = ''.join(input("Need original file?").split())
        downloadartworks(session, headers, id, savedir, len(isoriginal) == 0)
except Exception as e:
    print(e)
input()
