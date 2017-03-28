from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.shortcuts import render, redirect
from .make_url import make_url
from .models import Word
from django.http import HttpResponse, Http404
from . forms import UserLoginForm, CreateUserForm, UserImageForm
from django.views.generic import View
from django.contrib import messages

import os
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from .models import (
    Word,
    WordSearch
)



def make_anki_text(request):
    all_words = Word.objects.all()
    anki_header = Word.objects.first().anki_header()
    content = ''
    content += anki_header 

    for word in all_words:
        text = word.make_string()
        content += text

    with open("anki_doc.txt", 'w') as f:
        f.write(content)
        f.close()

    return HttpResponse(content, content_type='text/plain')


# def make_anki_text(request):

#     all_words = Word.objects.all()
#     anki_header = Word.objects.first().anki_header()
#     filename = "anki_doc.txt"

#     file = open(filename, "w")
#     file.write(anki_header)

#     for word in all_words:
#         text = word.make_string()
#         file.write(text)

#     file.close()
#     file_path = os.path.exists(os.getcwd() + '/auto_dict/' + filename)
#     # if os.path.exists(file_path):
#     #     with open(file_path, 'rb') as fh:
#     #         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#     #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#     #         return response
#     # else:
#     #     raise Http404

#     if os.path.exists(file_path):
#         f = open(file_path, 'r')
#         myfile = File(f)
#         response = HttpResponse(myfile, content_type='text/plain')
#         response['Content-Disposition'] = 'attachment; filename=' + 'anki_doc.txt'
#         return response
#     else:
#         raise Http404




    # return render(request, 'auto_dict/index.html')


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


    words = Word.objects.all()
    context = {'words': words}

    # we check to see if a post request
    # has been made.
    # if so, we need to look for the
    # information passed along to the
    # input named "word". Use that information
    # to search the dictionaryAPI and return to
    # our user the definition of the word
    if request.method == 'POST':
        word = request.POST.get('word', '')
        word_search = WordSearch(search=word)
        word_search.save()

        word = word.strip()
        url = make_url(word)


        # before we do the search
        # we check if the word
        # already exists
        for w in words:
            if w.word == word:
                print("word already searched " * 100)
                context['word'] = w
                return render(request,
                              'auto_dict/word_search.html',
                              context)

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

        

        word_obj = Word(word=word,
                        definition=my_def,
                        full_json_response=text,
                        )
        word_obj.save()

        word_obj.get_info()
        word_obj.save()

        context = {'word': word_obj}

        # this renders the template with some
        # return a context dictionary
        # that passes our templates
        # some pieces of information
        # (here, the definition
        # of the word that the user
        # pass us in the post request)
        return render(request, 'auto_dict/word_search.html', context)

    return render(request, 'auto_dict/word_search.html', context)

def index(request):
    return render(request, 'auto_dict/index.html')


def tables(request):
    return render(request, 'auto_dict/table.html')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'auto_dict/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('auto_dict:index')
            else:
                # An inactive account was used - no logging in!
                messages.error(request, 'Your account is disable')
                form = self.form_class(None)
                context = {'form': form}
                return render(request, self.template_name, context)

        messages.error(request, 'Your username or password did not match')
        form = self.form_class(None)
        context = {'form': form}
        return render(request, self.template_name, context)

class RegisterView(View):

    form_class = CreateUserForm
    template_name = 'auto_dict/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns User objects if credentilas are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    # change this. This is error
                    return redirect('auto_dict:index')

        return render(request, self.template_name, {'form': form})


@login_required(login_url='/auto_dict/login/')
def user_logout(request):
    logout(request)
    return redirect('auto_dict:index')


@login_required
def change_user_image(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)

        if form.is_valid():

            #if there is no user_profile create one
            try:
                user_profile = request.user.user_profile
            except Exception as the_exception:
                if the_exception.__str__() == "User has no user_profile.":
                    a = UserProfile(user=request.user)
                    a.save()
                    user_profile = a


            user_image = form.save(commit=False)
            user_image.save()


            user_profile.all_profile_pics.add(user_image)
            user_profile.profile_pic = user_image
            user_profile.save()            


            return redirect('auto_dict:index')


    return render(request, 'auto_dict/change_user_pic.html', {'form': UserImageForm()})