# a helper function
# to make your url
def make_url(word):
    # MAKE SURE YOU SET A
    # DICTIONARY_API_SECRET_KEY VARIABLE
    # IN YOUR SETTINGS.PY FILE
    # DICTIONARY_API_SECRET_KEY = "YOUR SECRET KEY!!"
    # FOR EXAMPLE
    # DICTIONARY_API_SECRET_KEY = "075n4nh-j53b-78b3-5439-8j56fgn3dce"
    secret_key = settings.DICTIONARY_API_SECRET_KEY

    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
    url += word + "?key=" + secret_key


    return url