import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from support.download import downloadfile

retrymark = True

def downloadfileset(session, urllist, localpath):
    global retrymark
    success = []
    failure = []
    for item in urllist:
        result = downloadfile(session, item, localpath)
        if len(result) == 0:
            failure.append(item)
        else:
            success.append(item)
        print('[success/failure/total]:{0}/{1}/{2}'.format(
            len(success), len(failure), len(urllist)))
    if len(failure) != 0:
        if retrymark:
            retrymark = False
            print("Retry download failed source.")
            downloadfileset(session, failure, localpath)

def downloadartworks(session, headers, illustsid, basedir, isregular):
    global retrymark
    retrymark = True

    if isregular:
        savedir = os.path.join(basedir, illustsid + "_regular")
    else:
        savedir = os.path.join(basedir, illustsid + "_original")

    if os.path.exists(savedir):
        if os.path.isfile(savedir):
            os.remove(savedir)
            os.makedirs(savedir)
    else:
        os.makedirs(savedir)

    headers['Referer'] = 'https://www.pixiv.net/artworks/{0}'.format(illustsid)
    headers['Accept'] = 'application/json'
    session.headers = headers

    result = session.get(
        'https://www.pixiv.net/ajax/illust/{0}/pages?lang=zh'.format(illustsid)).json()
    urllist = []
    for item in result['body']:
        if isregular:
            urllist.append(item['urls']['regular'])
        else:
            urllist.append(item['urls']['original'])

    headers['Referer'] = 'https://www.pixiv.net/'
    headers['Accept'] = 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    session.headers = headers
    downloadfileset(session, urllist, savedir)