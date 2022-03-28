import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pixiv.artworks import downloadartworks
from pixiv.user import initsession

def getillustsList(session, userid):
    result = session.get(
        'https://www.pixiv.net/ajax/user/{0}/profile/all?lang=zh'.format(userid)).json()
    illusts = []
    for key, value in result['body']['illusts'].items():
        illusts.append(key)
    print("Total:{0}".format(len(illusts)))
    return illusts

def traversecreator(session, headers, userid, basedir, isregular):
    illustslist = getillustsList(session, userid)
    for illusts in illustslist:
        downloadartworks(session, headers, illusts, basedir, isregular)

try:
    session, headers = initsession()
    if len(sys.argv) > 1:
        savedir = sys.argv[1]
        if len(savedir) == 0:
            savedir = os.path.split(os.path.realpath(__file__))[0]
    else:
        savedir = os.path.split(os.path.realpath(__file__))[0]
    while 1:
        id = ''.join(input("Input user id:").split())
        if len(id) == 0:
            break
        isoriginal = ''.join(input("Need original file?").split())

        downloadartworks(session, headers, id, savedir, len(isoriginal) == 0)
except Exception as e:
    print(e)
input()
