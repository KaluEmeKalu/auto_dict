from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen


def make_url(word):
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
    url += word + "?key=05b928bf-c814-4ee3-9762-020bf3dc8c2b"
    return url


def index(request):

    if request.method == 'POST':

        word = request.POST.get('word', '')
        if word:
            word = word.strip()

        url = make_url(word)

        # import pdb
        # pdb.set_trace()

        html = urlopen(url)
        text = html.read()

        if type(text) != type("string"):
            text = text.decode('utf-8')

        index = text.find("def")
        index = text.find("dt", index)
        index = text.find(":", index)
        end_index = text.find("</dt>", index)

        my_def = text[index:end_index]

        context = {'word': word, 'definition' : my_def}

        

        return render(request, 'auto_dict/index.html', context)

        


    return render(request, 'auto_dict/index.html')