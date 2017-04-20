##############################
#  Imports                   #
##############################

# django Imports
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Model
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models.signals import post_save
from django.db import models
from django.db.models import (
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    ImageField,
    DecimalField,
    BooleanField,
    TextField,
    OneToOneField,
    ManyToManyField,
    FileField
)

# python imports
import re
import math
import json

# others
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose
from bs4 import BeautifulSoup as BS

def delete_error_words(word_obj):
    error_words = [word for word in Word.objects.all(
    ) if "id API key or reference name provided" in word.definition]
    for word in error_words:
        word.delete()


##############################
# Upload Loaction  functions #
##############################
def step_image_upload_location(instance, filename):

    filename = str(filename.decode('utf-8'))

    return "steps/images/{}".format(filename)


def anki_import_textfiles_upload_location(instance, filename):
    return "anki_import_textfiles/{}".format(filename)


def step_file_upload_location(instance, filename):
    return "steps/files/{}".format(filename)


def audio_upload_location(instance, filename):
    return "audio/{}".format(filename)


def remove_tags_regex(string):
    return re.sub('<[^<]+?>', '', string)


def image_upload_location(instance, filename):
    return "images/{}".format(filename)


def venue_upload_location(instance, filename):
    return "{}, {}".format(instance.venue.name, filename)


def userprofile_upload_location(instance, filename):
    return "{}, {}".format(instance.user.username, filename)


def menu_upload_location(instance, filename):
    return "{}, Menu, {}".format(instance.venue.name, filename)


##############################
# Helper functions           #
##############################
def get_definition(xml_string):
    # find the word definition start and end indexes
    index = xml_string.find("def")
    index = xml_string.find("dt", index)
    start_index = xml_string.find(":", index) + 1
    end_index = xml_string.find("</dt>", start_index)

    # select the string containing the definition
    my_def = xml_string[start_index:end_index]

    return my_def


def get_html_contents(html_string, tag, index=None, many=None):

    if many:
        pass
        # content = get_html_contents(html_string, tag)
        # content_list = [content]

        # content_index = html_string.find(content)
        # next_index = html_string.find(tag, next_index)

        # while next_index != -1:
        #     temp_content = get_html_contents(html_string, tag,
        #                                      index=next_index)
        #     content_list.append(temp_content)
        #     content_index = html_string.find(content)
        #     next_index = html_string.find(tag, content_index)

        # return content_list
    else:
        try:
            open_tag = "<{}>".format(tag)
            close_tag = "</{}>".format(tag)

            if index:
                start = index
            else:
                start = 0
            start_index = html_string.find(open_tag, start) + len(open_tag)
            end_index = html_string.find(close_tag, start_index)
            content = html_string[start_index:end_index]
            return content
        except:
            return None


##############################
# Models                     #
##############################
class IntegerRangeField(IntegerField):
    def __init__(self, verbose_name=None, name=None,
                 min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Tag(Model):
    word = CharField(max_length=60)
    user = ForeignKey(User, related_name="tags", blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.word



class AnkiImportTextFile(Model):
    file = FileField(upload_to=anki_import_textfiles_upload_location)
    user = ForeignKey(User, related_name="anki_import_textfiles",
                      blank=True, null=True)
    title = CharField(max_length=80, null=True, blank=True)
    timestamp = DateTimeField(editable=False, auto_now_add=True,
                              auto_now=False, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class AudioRecording(Model):
    file = FileField(upload_to=audio_upload_location)
    user = ForeignKey(User, related_name="audio_recordings",
                      blank=True, null=True)
    title = CharField(max_length=80, null=True, blank=True)
    timestamp = DateTimeField(editable=False, auto_now_add=True,
                              auto_now=False, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title



class Question(Model):
    question = TextField(null=True, blank=True)
    exam = ForeignKey('Exam', related_name="questions", null=True, blank=True)
    question_number = IntegerField(blank=True, null=True)
    image = models.ForeignKey(
        'Image', null=True, blank=True, related_name='question')
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.question


class Answer(Model):
    answer = TextField(null=True, blank=True)
    question = ForeignKey('Question', related_name="answers")
    is_right_answer = BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.answer


class Exam(Model):
    created_by = ForeignKey(User, blank=True, null=True, related_name='exams')
    timestamp = DateTimeField(editable=False, auto_now_add=True,
                              auto_now=False, null=True, blank=True)
    name = CharField(max_length=80, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    school_class = ForeignKey('SchoolClass', blank=True,
                              null=True, related_name="exams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        isDS = settings.IS_DEPLOYMENT_SERVER
        try:
            dsURL = 'http://112.74.48.237/exam/'
            psURL = 'http://127.0.0.1:8000/exam/'
            url = dsURL if isDS else psURL
            return url + str(self.id)
        except Exception as e:
            raise Exception("""
                            Got Error {}.
                            Have you set the isDeploymentServer variable in settings.py?
                            """.format(e))


class ExamPaperHelper(Model):

    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_answered_questions(self):
        return [selection.answer.question for selection in self.selections.all()]

    def get_unanswered_questions(self):
        all_questions = self.exam.questions.all()
        answered_questions = self.get_answered_questions()
        return [question for question in all_questions if question not in answered_questions]

    def get_wrong_answers(self):
        return [selection.answer for selection in self.selections.all() if selection.answer.is_right_answer == False]

    def get_right_answers(self):
        return [selection.answer for selection in self.selections.all() if selection.answer.is_right_answer == True]

    def get_score(self, out_of_all_total_answers=True):
        correct_answers = len(self.get_right_answers())

        if out_of_all_total_answers:
            # total answers equals all exam questions
            total_questions = len(self.exam.questions.all())
        else:
            # total questions equals right answers + wrong answers
            total_questions = correct_answers + len(self.get_wrong_answers())

        score = float(correct_answers) / float(total_questions) * 100.0

        return round(score)

    class Meta:
        abstract = True

    def __str__(self):
        try:
            return "{} Exam: Exam Taker - {}. ".format(self.exam.name, self.exam_taker.username)
        except:
            return "Exam object {} created at {}".format(self.id, self.timestamp)


class ExamPaper(ExamPaperHelper):
    is_turned_in = BooleanField(default=False)
    exam_taker = ForeignKey(User, null=True, blank=True,
                            related_name="exam_papers")
    exam = ForeignKey(Exam, related_name="exam_papers")
    turn_in_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    final_score = IntegerField(null=True)



class TurnedInExam(Model):
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    final_score = IntegerField(null=True)
    exam_taker = ForeignKey(User, related_name="turned_in_exams", null=True)
    exam_paper = OneToOneField('ExamPaper', related_name='turned_in_exam',
                               null=True)


class Course(Model):
    name = CharField(max_length=160)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name




class SchoolClass(Model):
    name = CharField(max_length=160)
    teacher = ForeignKey(User, blank=True, null=True,
                         related_name="teacher_classes")
    students = ManyToManyField(
        User, blank=True, related_name="student_classes")
    course = ForeignKey('Course', null=True, blank=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    private = BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_percentage_completed(self):
        """
        Returns a percentage float of representing
        total videos watched / total step videos
        """

        # get list of ratio dictionaries from steps
        ratio_watched_list = [step.get_ratio_watched() for step in self.steps.all()]

        total = 0
        watched = 0

        # loop through list and increment total and watched
        for ratio in ratio_watched_list:
            watched += ratio['watched']
            total += ratio['total']

        # return percentage            
        try:
            percentage = float(watched) / total
            percentage = int(round(percentage * 100))
            return percentage
        except:
            return 0



    def get_json_points_data(self):
        """
        returns a json list of key-value pairs
        of students and class points, each
        list will have the keys-value pairs:
           label:"some_username", 
           value: *some integer* (see custom.js)
        """
        pass
        students = self.students.all()
        json_list = []
        for student in students:
            points = get_achievement_points(student)
            my_dict = {'label': student.username,
                       'value': points}
            json_list.append(my_dict)

        return json.dumps(json_list)


    def give_students_class_achievement(self):

        students = self.students.all()
        try:
            # Try to get class start achievement
            # if this achievement hasn't been made yet
            # then there will be an exception
            achievement  = Achievement.objects.get(school_class=self, 
                                                  name="Class Start Achievement")
        except:
            # exception if class start achievement doesn't exist
            # then we create the class start acheivement
            message = "Welcome to the start of a new learning adventure!"
            achievement = Achievement(name="Class Start Achievement",
                                      points=5, message=message,
                                      school_class=self)
            achievement.save()

        for student in students:

            # We try to get the class start achievement relation record for the user
            # if it doesn't exist we create a new record.
            try:
                UserAchievement.objects.get(user=student,
                                            achievement=achievement)
            except:
                UserAchievement(user=student, achievement=achievement).save()



    def __str__(self):
        try:
            return "{} with {}".format(self.name, self.teacher.first_name, self.teacher.last_name)
        except:
            return self.name

    class Meta:
        verbose_name_plural = "School Classes"


class AbstractSelection(Model):
    answer = ForeignKey("Answer", related_name="selections")
    exam_paper = ForeignKey(
        "ExamPaper", related_name="selections", null=True, blank=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.answer.answer

    class Meta:
        abstract = True



class Selection(AbstractSelection):
    pass



class OldSelection(AbstractSelection):
    answer = ForeignKey("Answer", related_name="old_selections",
                        blank=True, null=True)
    exam_paper = ForeignKey(
        "ExamPaper", related_name="old_selections", null=True, blank=True)
    old_timestamp = models.DateTimeField(blank=True, null=True)
    old_updated_timestamp = models.DateTimeField(blank=True, null=True)


class Word(Model):
    created_by = ForeignKey(User, blank=True, null=True)
    word = CharField(max_length=160, default="No Word Entry")
    definition = TextField(default="No Definition Entry")
    example = TextField(default="No Example Entry")
    origin = TextField(default="No Origin Entry")
    part_of_speech = TextField(
        null=True, blank=True, default="No Part Of Speech Entry")
    syllables = TextField(default="No Syllables Entry")
    synonyms = TextField(default="No Synonyms Entry")
    antonyms = TextField(default="No Antonyms Entry")
    other_usages = TextField(null=True, blank=True,
                             default="No Other Usages Entry")
    pronunciation = TextField(null=True, blank=True,
                              default="No Pronunciation Entry")
    tags = TextField(default="No Tags Entry")
    audio = TextField(default="No Audio Entry")
    full_json_response = TextField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    isPopulated = BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def remove_html_tags(self, all_words=False):

        # check if word argument passed
        if all_words is True:
            words = Word.objects.all()
            for word in words:
                word.remove_html_tags()
        else:
            self.origin = re.sub('<[^<]+?>', '', self.origin)
            self.part_of_speech = re.sub('<[^<]+?>', '', self.part_of_speech)
            self.syllables = re.sub('<[^<]+?>', '', self.syllables)
            self.synonyms = re.sub('<[^<]+?>', '', self.synonyms)
            self.antonyms = re.sub('<[^<]+?>', '', self.antonyms)
            self.other_usages = re.sub('<[^<]+?>', '', self.other_usages)
            self.pronunciation = re.sub('<[^<]+?>', '', self.pronunciation)
            self.tags = re.sub('<[^<]+?>', '', self.tags)
            self.definition = re.sub('<[^<]+?>', '', self.definition)

            self.save()

    def populate_fields(self):
        json = self.full_json_response

        soup = BS(json).entry

        # get examples

        try:
            example = soup.dt.vi.extract() # extract from definition
            self.example = str(example.text.encode('utf-8'))
        except:
            pass            
        


        # get prounciation
        try:
            self.pronunciation = str(soup.pr.text.encode('utf-8'))
        except:
            self.pronunciation = "No Pronunciation saved."

        # get part of speech
        try:
            self.part_of_speech = str(soup.fl.text.encode('utf-8'))
        except:
            self.part_of_speech = "No Part of Speech"

        # get origin
        try:
            self.origin = str(soup.et.text.encode('utf-8'))
        except:
            self.origin = "No Origin Saved"


        # get syllables
        try:
            self.syllables = str(soup.hw.text.encode('utf-8'))
        except:
            self.syllables = "No Syllables saved."

        # get other_usages
        try:
            # uro stands for undefined run-on entry
            uros = soup.find_all('uro')
            # import pdb; pdb.set_trace()
            other_usages_string = ""
            for index, uro in enumerate(uros):

                # add other-usage word
                temp_str = str(uro.ure.text.encode('utf-8'))

                # add part of speech of the word.
                temp_str += ": " + str(uro.fl.text.encode('utf-8'))

                # add comma if not the last one.
                if index != len(uros) -1:
                    temp_str += ", "

                other_usages_string += temp_str
            self.other_usages = other_usages_string
        except Exception as e:
            print("Exception {}. Saved as no other usages instead. \n\n".format(e) * 10)
            self.other_usages = "No Other Usages"



        try:
            definitions = soup.find_all('def')[0].find_all('dt')

            # get defintion
            count = 1
            definition_string = ''
            for definition in definitions:
                temp_def_text = " {} - ".format(count)
                temp_def_text += str(definition.text[1:].encode('utf-8'))

                definition_string += temp_def_text
                count += 1
            self.definition = definition_string
        except:
            pass
            # this is a weird error, handle for it later.
            # can't think of why there wouldn't be any def





        self.isPopulated = True

        try:
            self.save()
        except:
            raise Exception("There was problem saving!")
        return json



    def populate_fields_old(self):
        json = self.full_json_response


        # get prounciation
        pronunciation = get_html_contents(json, 'wpr')
        self.pronunciation = remove_tags_regex(pronunciation)

        # get part of speech
        part_of_speech = get_html_contents(json, 'fl')
        self.part_of_speech = remove_tags_regex(part_of_speech)

        # get origin
        origin = get_html_contents(json, 'et')
        self.origin = remove_tags_regex(origin)

        # get other_usages
        other_usages = get_html_contents(json, 'uro')
        if other_usages:
            self.other_usages = remove_tags_regex(other_usages)

        # get syllables
        syllables = get_html_contents(json, 'hw')
        self.syllables = remove_tags_regex(syllables)

        # get definition
        definition = get_html_contents(json, 'dt')
        definition = definition[1:]  # removes the colon
        self.definition = remove_tags_regex(definition)

        self.isPopulated = True

        try:
            self.save()
        except:
            raise Exception("There was problem saving!")
        return json

    # This runs upon save populated fieds
    # if they haven't previously been
    # populated.
    def save(self, *args, **kwargs):
        if not self.isPopulated:
            self.populate_fields()

        super(Word, self).save(*args, **kwargs)

    def anki_header(self):
        text = "Front\tBack\t"
        text += "Part of speech\tSyllables\t"
        text += "Origin\t"
        text += "Used in sentence\t"
        text += "Synonyms\tAntonyms\t"
        text += "Other usages\tPronunciation\tTags\n\n"
        return text

    def make_string(self):
        word = self
        entry = "{}\t{}\t".format(word.word.encode('utf8'), word.definition.encode('utf8'))
        entry += "{}\t".format(word.part_of_speech.encode('utf8'))
        entry += "{}\t".format(word.syllables.encode('utf8'))
        entry += "{}\t".format(word.origin.encode('utf8'))
        entry += "{}\t".format(word.example.encode('utf8'))
        entry += "{}\t".format(word.synonyms.encode('utf8'))
        entry += "{}\t".format(word.antonyms.encode('utf8'))
        entry += "{}\t".format(word.other_usages.encode('utf8'))
        entry += "{}\t".format(word.pronunciation.encode('utf8'))
        entry += "{}\n".format(word)
        entry += "\n"
        return entry

    def __str__(self):
        return self.word

    def time_ago(self):
        return naturaltime(self.timestamp)


class Video(Model):
    file = FileField(null=True, blank=True, upload_to=step_file_upload_location)
    name = CharField(max_length=180, blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    order = models.IntegerField(default=0)
    watched = BooleanField(default=False)

    def time_ago(self):
        return naturaltime(self.timestamp)

    def __str__(self):

        try:
            name = '{} Submitted Image on {}'.format(self.name, self.timestamp)
        except:
            name = 'Submitted Image on {}'.format(self.timestamp)
        return name


    class Meta:
        ordering = ['order', ]
        

class Step(Model):
    name = CharField(max_length=180, blank=True, null=True)
    school_class = ForeignKey('SchoolClass', blank=True, null=True,
                              related_name='steps')
    description = TextField(blank=True, default='')
    order = models.IntegerField(default=0)
    url = CharField(max_length=300, blank=True, null=True)

    video = FileField(null=True, blank=True, upload_to=step_file_upload_location)
    images = models.ManyToManyField('Image', blank=True,
                              related_name='steps')
    videos = models.ManyToManyField('Video', blank=True,
                              related_name='steps')
    exam = ForeignKey('Exam', related_name='steps', null=True, blank=True)
    articles = ManyToManyField('Article', related_name="steps", blank=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_ratio_watched(self):
        """
        Returns a dictionary with ratio of watched to unwatched
        videos for the step.

        The return will be used by SchoolClass method 
        which will calculate percentage watched for all videos
        """
        videos = self.videos.all()
        watched_videos = len([video for video in videos if video.watched])
        ratio_watched = {'watched': watched_videos, 'total': len(videos)}

        return ratio_watched




    def get_href(self):
        # if self.exam:
            #return exam url
            # pass
        return "#step{}".format(self.id)

    def get_articles(self):
        """
        return colleciton of articles if exists,
        if not returns empty list
        """
        try:
            all_articles = self.articles.all()
            return all_articles
        except:
            return []



    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.name

    def time_ago(self):
        return naturaltime(self.timestamp)



class Article(Model):
    texts = ManyToManyField('Text', related_name="articles", blank=True)
    title = CharField(max_length=180, blank=True, null=True)

    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    order = IntegerField(default=0)
    url = CharField(max_length=300, blank=True, null=True)
    image = models.ForeignKey('Image', null=True, blank=True,
                              related_name='articles')


    def get_texts(self):
        """
        return colleciton of articles if exists,
        if not returns empty list
        """
        try:
            all_texts = self.texts.all()
            return all_texts
        except:
            return []

    def __str__(self):
        return self.title

    def time_ago(self):
        return naturaltime(self.timestamp)

    class Meta:
        ordering = ['order']

class Text(Model):
    title = CharField(max_length=180, blank=True, null=True)
    content = TextField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = DateTimeField(auto_now=True, blank=True, null=True)
    order = IntegerField(default=0)

    def __str__(self):
        return self.title

    def time_ago(self):
        return naturaltime(self.timestamp)

    class Meta:
        ordering = ['order']


class Achievement(Model):
    points = IntegerField(null=True, blank=True)
    name = CharField(max_length=180, blank=True, null=True)
    message = CharField(max_length=300, blank=True, null=True)
    school_class = ForeignKey('SchoolClass', null=True, blank=True,
                              related_name="achievements")
    created_by = ForeignKey(User, null=True, blank=True,
                            related_name='achievements_created')
    step = ForeignKey('Step', null=True, blank=True,
                      related_name="achievements")
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)



    def __str__(self):
        return self.name

    def time_ago(self):
        return naturaltime(self.timestamp)



def get_achievement_points(user_obj):
    achievements = user_obj.user_achievements.all()

    points = 0
    for user_achievement in achievements:
        points += user_achievement.achievement.points
    return points 
    

class StepAchievementTable(Model):
    pass



class UserAchievement(Model):
    user = ForeignKey(User, null=True, blank=True,
                      related_name="user_achievements")
    achievement = ForeignKey('Achievement', null=True, blank=True,
                             related_name="user_achievements")

    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        try:
            return '{} Achievement for {}. '.format(self.achievement.name, self.user.username)
        except:
            return "No string available."

    def time_ago(self):
        return naturaltime(self.timestamp)




class Post(Model):
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    content = TextField(null=True, blank=True)
    user = ForeignKey(User, related_name='posts', blank=True, null=True)
    school_class = ForeignKey("SchoolClass", related_name="posts")

    def __str__(self):
        return self.content

    def time_ago(self):
        return naturaltime(self.timestamp)

    def get_absolute_url(self):
        return '/class/{}'.format(self.school_class.id)

class WordSearch(Model):
    searched_by = ForeignKey(User, blank=True, null=True)
    search = CharField(max_length=180, default="No Search Entry")
    words = ManyToManyField('Word', blank=True)
    times_searched = IntegerField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.word

    def time_ago(self):
        return naturaltime(self.timestamp)


class Address(Model):
    address_1 = CharField(max_length=128)
    address_2 = CharField(max_length=128, blank=True)
    city = CharField(max_length=64)
    state = CharField(max_length=128)  # add validator
    zip_code = CharField(max_length=5)
    country = CharField(max_length=128, null=True, blank=True)
    area_of_city = CharField(max_length=128, null=True, blank=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.address_1

    def time_ago(self):
        return naturaltime(self.timestamp)


class Venue(Model):
    name = CharField(max_length=200)
    user = ForeignKey(User, related_name="venues", null=True, blank=True)
    address = ForeignKey(Address, related_name="venues")
    description = CharField(max_length=500)

    average_cost = DecimalField(max_digits=6, decimal_places=2)

    sit_in_available = BooleanField(default=False)
    delivery_available = BooleanField(default=False)
    pick_up_available = BooleanField(default=False)
    is_banned = BooleanField(default=False)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    my_namespace = CharField(
        default="Venue", max_length=128, null=True, blank=True)
    tags = ManyToManyField(Tag, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def time_ago(self):
        return naturaltime(self.timestamp)


class Review(Model):
    comment = TextField()
    user = ForeignKey(User, related_name="reviews")
    rating = IntegerRangeField(min_value=1, max_value=5)
    is_banned = BooleanField(default=False)
    venue = ForeignKey(Venue, related_name="reviews")
    timestamp = models.DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    my_namespace = CharField(
        default="Review", max_length=128, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.comment)

    def time_ago(self):
        return naturaltime(self.timestamp)


class Image(models.Model):
    # user = OneToOneField(User, related_name="image", null=True, blank=True)
    # content_object = GenericForeignKey('content_type', 'object_id')
    image = ProcessedImageField(processors=[  # ResizeToFill(
        # 100, 50),
        Transpose()],
        upload_to=image_upload_location,
        null=True,
        blank=True,
        format='JPEG',
        options={'quality': 60})
    my_namespace = CharField(
        default="Image", max_length=128, null=True, blank=True)
    timestamp = DateTimeField(editable=False, auto_now_add=True,
                              auto_now=False, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):

        return 'Submitted Image on {}'.format(self.timestamp)

    def time_ago(self):
        return naturaltime(self.timestamp)


def make_all_user_profiles(users_profiles=False, teachers_profiles=False, student_profiles=False):
    """
    Will create all user profiles by default if any are not yet created,
    if argument variable student_profiles is passed in
    and set as True then it will create all student_profiles
    """

    def make_profiles(ProfileObject, users):
        for user in users:
            try:
                u = ProfileObject(user=user)
                u.save()
            except Exception as e:
                print("\n\n{} profiles were not created \n\n".format(ProfileObject) * 10)


    if users_profiles is True:
        # create all user profiles
        ProfileObject = UserProfile
        users = User.objects.all()
        make_profiles(ProfileObject, users)
    elif student_profiles is True:
        # create all student profiles
        ProfileObject = StudentProfile
        users = [user for user in User.objects.all(
        ) if user.user_profile.is_student is True]
        make_profiles(ProfileObject, users)
    else:
        # create both user and student profiles

        # first create User Profiles
        ProfileObject = UserProfile
        users = User.objects.all()
        make_profiles(ProfileObject, users)

        # then student Profiles
        ProfileObject = StudentProfile
        users = [user for user in User.objects.all(
        ) if user.user_profile.is_student is True]
        make_profiles(ProfileObject, users)

        #then students
        ProfileObject = TeacherProfile
        users = [user for user in User.objects.all(
        ) if user.user_profile.is_teacher is True]
        make_profiles(ProfileObject, users)



class TeacherProfile(models.Model):
    user = OneToOneField(User, related_name="teacher_profile")
    courses = ManyToManyField('Course', related_name='teachers_profiles',
                               blank=True)

    def __str__(self):
        return self.user.username

    def get_image_url(self):
        return self.user.user_profile.profile_pic.image.url


class StudentProfile(models.Model):
    user = OneToOneField(User, related_name="student_profile")
    year = IntegerField(blank=True, null=True)
    gpa = IntegerField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def get_image_url(self):
        return self.user.user_profile.profile_pic.image.url


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    profile_pic = models.ForeignKey(
        'Image', null=True, blank=True, related_name='user_profile')
    all_profile_pics = models.ManyToManyField(
        'Image', blank=True, related_name="user_profiles")
    is_student = BooleanField(default=True)
    is_teacher = BooleanField(default=False)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    points = IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def get_image_url(self):

        try:
            url = self.profile_pic.image.url 
            return url
        except AttributeError as e:
            # return default user url
            url = static('auto_dict/img/find_user.png')
            return url


# ...  u.profile_pic.image
# ... except AttributeError as e:
# ...  print("You got errror {} .!".format(e))


def create_user_profile(sender, **kwargs):
    """Creates a User Profile upon creation of User"""
    user = kwargs['instance']
    if kwargs['created']:
        user_profile = UserProfile(user=user)
        user_profile.save()
        try:
            if user.is_student == True:
                student_profile = StudentProfile(user=user)
                student_profile.save()
        except:
            pass


post_save.connect(create_user_profile, sender=User)
