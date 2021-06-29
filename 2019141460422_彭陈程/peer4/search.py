from load import geturl
def search(keyword):
    url=geturl()
    filepaths=[]
    for url_one in url:
        if url_one.find(keyword) == -1:
            pass#什么都不做
        else:
            filepaths.append(url_one)
    return filepaths