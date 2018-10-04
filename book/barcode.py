import urllib.request
from xml.etree.ElementTree import parse
from pyzbar import pyzbar
import cv2

def barcode_read(image):
    image = cv2.imread(image)
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        text = "{}".format(barcodeData)
    try:
        return parsing(text)
    except UnboundLocalError:
        return "Please input right barcode image"

def parsing(isbn):
    client_id = "niB9_CXggiK8A3eGJZAp"
    client_secret = "bBP1MSFPxE"
    encText = urllib.parse.quote(isbn)
    url = "https://openapi.naver.com/v1/search/book_adv.xml?d_isbn=" + encText # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        data = parse(response)
        return py_xml_proc(data)
    else:
        print("Error Code:" + rescode)

def py_xml_proc(data):
    b_data = {}
    for item in data.iterfind('channel/item'):
        b_data['title'] = item.findtext('title')
        b_data['author'] = item.findtext('author')
        b_data['publisher'] = item.findtext('publisher')
        b_data['pubdate'] = item.findtext('pubdate')
        b_data['price'] = item.findtext('price')
        b_data['image'] = item.findtext('image')
    return b_data
