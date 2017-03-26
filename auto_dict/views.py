from django.shortcuts import render
from .make_url import make_url
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen




# your index view.
# views
# 1)provides the logic
# for your webpage,
# 2) passes information
# from and to your 
# users (with get and post)
# requests,
# and 
# 3 tells the webpage which
# html template to use.
def word_search(request):


    # we check to see if a post request
    # has been made. 
    # if so, we need to look for the 
    # information passed along to the
    # input named "word". Use that information
    # to search the dictionaryAPI and return to
    # our user the definition of the word
    if request.method == 'POST':
        word = request.POST.get('word', '').strip()
        url = make_url(word)
        html = urlopen(url)
        text = html.read()

        # if text is not a string,
        # (i.e., if it's bytes),
        # convert it to unicode string
        if not isinstance(text, type("string")):
            text = text.decode('utf-8')

        # find the word definition start
        # and end indexes
        index = text.find("def")
        index = text.find("dt", index)
        start_index = text.find(":", index) + 1
        end_index = text.find("</dt>", start_index)

        # select the string containing the definition
        my_def = text[start_index:end_index]

        context = {'word': word, 'definition': my_def}

        # this renders the template with some 
        # return a context dictionary
        # that passes our templates
        # some pieces of information
        # (here, the definition
        # of the word that the user 
        # pass us in the post request)
        return render(request, 'auto_dict/word_search.html', context)

    return render(request, 'auto_dict/word_search.html')


def index(request):
    return render(request, 'auto_dict/index.html')