import os


def downloadfile(session, url, dir):
    filename = url.split('/')[-1]
    waitingfile = os.path.join(dir, "waiting_" + filename)
    savefile = os.path.join(dir, filename)

    if os.path.exists(savefile):
        print('[skip]{0} already exists.'.format(savefile))
        return savefile

    try:
        r = session.get(url, stream=True)
        if r.status_code != 200:
            print('[fail]code:{0}'.format(r.status_code))
            return ""
    except Exception as e:
        print('[fail] error:{0}'.format(e))
        return ""

    size = 0
    totalsize = int(r.headers.get('content-length', 0))
    if totalsize >= 1024:
        chunk_size = 1024
        unit = "KB"
    else:
        chunk_size = 1
        unit = "Byte"

    if os.path.exists(waitingfile):
        if totalsize == os.path.getsize(waitingfile):
            os.rename(waitingfile, savefile)
            print('[skip]{} check over.'.format(savefile))
            return savefile
        else:
            os.remove(waitingfile)

    info = '{0}({1:.2f}{2})'.format(
        filename, float(totalsize / chunk_size), unit)

    with open(waitingfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            try:
                if chunk:
                    f.write(chunk)
                    size += len(chunk)
                    print('\r[{0}]{1:.0f}% | {2}'.format(
                        '#' * int(size * 30 / totalsize) + ' ' * (30 - int(size * 30 / totalsize)), float(size / totalsize * 100), info), end='')

            except Exception as e:
                print('[fail] error:{0}'.format(e))
                return ""
    print()
    if totalsize == os.path.getsize(waitingfile):
        os.rename(waitingfile, savefile)

    else:
        os.remove(waitingfile)
        print('[fail] size error.')
        return ""
    return savefile
