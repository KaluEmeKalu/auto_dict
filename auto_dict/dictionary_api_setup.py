from django.conf import settings
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen


def bytes_to_string(bytes_obj):
    # if text is not a string,
    # (i.e., if it's bytes),
    # convert it to unicode string
    if not isinstance(bytes_obj, type("string")):
        bytes_obj = bytes_obj.decode('utf-8')
        return bytes_obj
    else:
return bytes_obj


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



def get_xml_string(word):
    """
    Takes a word
    returns xml string of dictionaryapi
    webstersdict collegiate dict
    response
    """

    url = make_url(word)
    print("\nAttempting to open URL: {}\n\n".format(url))
    html = urlopen(url)
    print("\nYay!! URL OPENED!!!\n\n")
    xml_string = html.read()
    print("\nYay!! URL READ!!!!!\n\n")

    # if text is not a string,
    # (i.e., if it's bytes),
    # convert it to unicode string
    xml_string = bytes_to_string(xml_string)

    return xml_string


def get_definition(xml_string):
    # find the word definition start and end indexes
    index = xml_string.find("def")
    index = xml_string.find("dt", index)
    start_index = xml_string.find(":", index) + 1
    end_index = xml_string.find("</dt>", start_index)

    # select the string containing the definition
    my_def = xml_string[start_index:end_index]

    return my_def