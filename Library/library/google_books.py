from django.utils import simplejson
from urllib2 import urlopen

def search(barcode):
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:%s" % barcode
    data_string = urlopen(url).read()
    google_data = simplejson.loads(data_string).get('items',[])
    response = {'book_list': []}
    for item in google_data:
        try:
            info = item['volumeInfo']
            book = {'image_link' : info['imageLinks']['thumbnail'],
                    'author' : info['authors'][0],
                    'title' : info['title'],
                    'barcode' : barcode}
            response['book_list'].append(book)
        except:
            pass
    return response