

def google_translate(url):
    urlstart = ""
    urlend = ""
    if url.startswith("https://"):
        urlstart = url.split("https://")[1]
        url = urlstart
    elif url.startswith("http://"):
        urlstart = url.split("http://")[1]
        url = urlstart

    try:
        urlstart = url.split("/", 1)[0]
        urlend = url.split("/", 1)[1]
    except:
        pass
    return f"https://{urlstart.replace('.', '-')}.translate.goog/{urlend}?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US"


def inverse_google_translate(url):
    try:
        front = url.split(".translate.goog")[0].replace('-', '.')
        back = url.split(".translate.goog")[1].split("?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US")[0]
        return front+back
    except IndexError:
        return url


def determine_bypass_url(url, bypassID):
    if bypassID == 1:
        return google_translate(url)

