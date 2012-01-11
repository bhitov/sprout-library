from django.utils import simplejson
from urllib2 import urlopen

def search(barcode):
    print "in search"
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:%s" % barcode
    print 'start urlopen'
    data_string = urlopen(url).read()
    print 'done with urlopen'
    google_data = simplejson.loads(data_string).get('items',[])
    response = {'book_list': []}
    print google_data
    print 'huh'
    for item in google_data:
        print 'what'
        try:
            info = item['volumeInfo']
            book = {'image_link' : info['imageLinks']['thumbnail'],
                    'author' : info['authors'][0],
                    'title' : info['title'],
                    'barcode' : barcode}
            response['book_list'].append(book)
        except:
            pass
        #response['book_list'].append(book)
    print response
    return response