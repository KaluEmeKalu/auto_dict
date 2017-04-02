from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from .make_url import make_url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from . forms import UserLoginForm, CreateUserForm, UserImageForm
from django.views.generic import View
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse
from datetime import datetime

import os, json
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from .models import (
    Word,
    WordSearch,
    ExamPaper,
    Exam,
    Selection,
    OldSelection,
    Answer,
    make_all_user_profiles
)


def bytes_to_string(bytes_obj):
    # if text is not a string,
    # (i.e., if it's bytes),
    # convert it to unicode string
    if not isinstance(bytes_obj, type("string")):
        bytes_obj = bytes_obj.decode('utf-8')
        return bytes_obj
    else:
        return bytes_obj


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


def get_definition(xml_string):
    # find the word definition start and end indexes
    index = xml_string.find("def")
    index = xml_string.find("dt", index)
    start_index = xml_string.find(":", index) + 1
    end_index = xml_string.find("</dt>", start_index)

    # select the string containing the definition
    my_def = xml_string[start_index:end_index]

    return my_def


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


def wordExists(word):
    """
    Takes a word string
    checks to see if word 
    exists in Word class 
    if so, then returns True
    if not returns False
    """
    words = Word.objects.all()

    exists = False

    # before we do the search
    # we check if the word
    # already exists
    for w_obj in words:
        if w_obj.word == word.strip():
            exists = True
            break

    return exists


def make_word_model(word_string):
    """
    Takes a string of a word,
    searches that string and
    returns a Word class object
    as defined in models.py
    """
    word = word_string

    # before we do the search
    # we check if the word
    # already exists
    if wordExists(word):
        print("\nword already searched\n " * 20)
        return Word.objects.filter(word=word).first()
    else:
        xml_string = get_xml_string(word)
        my_def = get_definition(xml_string)
        word_obj = Word(word=word,
                        definition=my_def,
                        full_json_response=xml_string,
                        )
        word_obj.save()
        return word_obj


def make_multiple_word_models(word_list):
    """
    Takes a list of strings of a word,
    searches those strings and
    returns a list of Word class object
    as defined in models.py
    """
    return [make_word_model(word) for word in word_list]


def get_wordlist_from_textstring(string):
    """
    Takes a string of comma delimited list of
    words and returns a list of those words
    """

    # get list of strings split by a comma
    word_list = string.split(',')
    # remove empty strings
    word_list = [word.strip() for word in word_list if word.strip()]

    return word_list


def turn_in_exam(request, exam_paper_id):


    exam_paper = ExamPaper.objects.get(pk=exam_paper_id)
    exam_paper.is_turned_in = True
    exam_paper.save()
    exam_id = exam_paper.exam.id
    exam = Exam.objects.get(id=exam_id)

    context = {'exam': exam, 'exam_paper': exam_paper}

    return render(request, 'auto_dict/exam.html', context)


    return HttpResponse("chill")



# class SaveAudio(CreateView):
    # model = AudioRecording
    # template_name = 'portals/create_audio.html'
    # fields = [
    #     'title',
    #     'file',

    # ]

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     print(self)

    #     context = super(SaveAudio, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['key_sentence'] = int(self.kwargs['key_sentence'])
    #     return context

    #def form_valid(self, form):
        # key_sentence = KeySentence.objects.get(pk=self.kwargs['key_sentence'])
        #form.save()
        #form.user = self.request.user
        # there's a mistake on this line
        # form.instance.key_sentences.add(key_sentence)
        #form.save()
        #print("Audio added " * 88)

        # return redirect('portals:index')


def save_answer(request):


    if request.method == 'POST':


        answer_id = request.POST.get('answer_id', '').strip()
        exam_paper_id = request.POST.get('exam_paper_id', '').strip()

        answer_obj = Answer.objects.get(id=answer_id)
        exam_paper_obj = ExamPaper.objects.get(pk=exam_paper_id)

        prev_selection = Selection.objects.filter(answer=answer_obj,
                                                  exam_paper=exam_paper_obj)

        all_selections = Selection.objects.filter(exam_paper=exam_paper_obj)
        
        # Check if question answered before
        questionAnsweredBefore = False
        for selection in all_selections:
            if answer_obj.question == selection.answer.question:
                questionAnsweredBefore = True

                # if answered before save selection obj
                selection_obj = selection

        if questionAnsweredBefore:
            # if previously answered, change answer.
            s = selection_obj
            old_selection_obj = OldSelection(answer=s.answer,
                                             exam_paper=s.exam_paper,
                                             old_timestamp=s.timestamp)
            old_selection_obj.save()
            selection_obj.answer = answer_obj
            selection_obj.save()
            print("Edited old selected! " * 50)
        else:
        
            # if not previsouly answered, make new selection
            import pdb; pdb.set_trace()
            selection_obj = Selection(answer=answer_obj,
                                  exam_paper=exam_paper_obj)
            selection_obj.save()
            print("Created new selected! " * 50)


        save_answer = selection_obj.answer.answer
        response_data = {'the_status': "all is great!", 'saved_answer': save_answer}

        # except:
        #     response_data['result'] = 'Oh No!'
        #     response_data['message'] = 'The script did not work properly'

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Exception("Wasn't able to save answer")





def exam(request, exam_id, turn_in=False):

    exam = get_object_or_404(Exam, pk=int(exam_id))
    exam_taker = request.user

    if turn_in == 'yes' or turn_in == 'true':

        exam_paper = ExamPaper.objects.get(exam_taker=exam_taker, exam=exam)
        exam_paper.is_turned_in = True
        exam_paper.save()

        context = {'exam': exam, 'exam_paper': exam_paper}

        return render(request, 'auto_dict/exam.html', context)

    

    # get exam_paper if previous existed
    # if none create an exam paper
    try:
        exam_paper = ExamPaper.objects.get(exam_taker=exam_taker, exam=exam)
    except ExamPaper.DoesNotExist:
        exam_paper = ExamPaper(exam_taker=exam_taker, exam=exam)
        exam_paper.save()

    context = {'exam': exam, 'exam_paper': exam_paper}

    if request.method == 'POST':
        pass

    return render(request, 'auto_dict/exam.html', context)


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

        if len(request.FILES) != 0:
            # if there files get the files
            # read them
            # and save them as Word models
            text = request.FILES['file'].read()
            text = bytes_to_string(text)
            wordlist = get_wordlist_from_textstring(text)
            found_words = make_multiple_word_models(wordlist)
            context['found_words'] = found_words

            return render(request, 'auto_dict/word_search.html', context)
        else:
            # else, if there are no files
            # that means there's a text input
            #, get the single word and save it
            # as a Word model. Then pass it to
            # the context as "found words" a list
            # wiht a single word object.
            word = request.POST.get('word', '').lower()

            word_search = WordSearch(search=word)
            word_search.save()
            word = word.strip()

            word_obj = make_word_model(word)
            context['found_words'] = [word_obj]

            # this renders the template with some
            # return a context dictionary
            # that passes our templates
            # some pieces of information
            # (here, the definition
            # of the word that the user
            # pass us in the post request)
            return render(request, 'auto_dict/word_search.html', context)

    return render(request, 'auto_dict/word_search.html', context)


def textfile_word_search(request):
    words = Word.objects.all()
    context = {'words': words}
    import pdb
    pdb.set_trace()

    if request.method == 'POST':
        text = request.FILES['file'].read()


def index(request):
    make_all_user_profiles()
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

            # if there is no user_profile create one
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
