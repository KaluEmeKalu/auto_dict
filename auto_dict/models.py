from django.db.models import Model
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models.signals import post_save

# Create your models here.
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
    ManyToManyField


)

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose

from django.db import models


def image_upload_location(instance, filename):
    return "{}".format(filename)


class IntegerRangeField(IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


def venue_upload_location(instance, filename):
    return "{}, {}".format(instance.venue.name, filename)


def userprofile_upload_location(instance, filename):
    return "{}, {}".format(instance.user.username, filename)


def menu_upload_location(instance, filename):
    return "{}, Menu, {}".format(instance.venue.name, filename)


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


class Tag(Model):
    word = CharField(max_length=60)
    user = ForeignKey(User, related_name="tags", blank=True, null=True)

    def __str__(self):
        return self.word


class Word(Model):
    created_by = ForeignKey(User, blank=True, null=True)
    word = CharField(max_length=160, default="No Word Entry")
    definition = TextField(default="No Definition Entry")
    example = TextField(default="No Example Entry")
    origin = TextField(default="No Origin Entry")
    part_of_speech = TextField(null=True, blank=True, default="No Part Of Speech Entry")
    syllables = TextField(default="No Syllables Entry")
    synonyms = TextField(default="No Synonyms Entry")
    antonyms = TextField(default="No Antonyms Entry")
    other_usages = TextField(null=True, blank=True, default="No Other Usages Entry")
    pronunciation = TextField(null=True, blank=True, default="No Pronunciation Entry")
    tags = TextField(default="No Tags Entry")
    audio = TextField(default="No Audio Entry")
    full_json_response = TextField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)


    def get_info(self):
        json = self.full_json_response

        #get prounciation
        pronunciation = get_html_contents(json, 'wpr')
        self.pronunciation = pronunciation

        # get part of speech
        part_of_speech = get_html_contents(json, 'fl')
        self.part_of_speech = part_of_speech

        # get origin
        origin = get_html_contents(json, 'et')
        self.origin = origin

        #get other_usages
        other_usages = get_html_contents(json, 'uro')
        if other_usages:
            self.other_usages = other_usages

         #get syllables
        syllables = get_html_contents(json, 'hw')
        self.syllables = syllables

        try:
            self.save()
        except:
            pass
        return json

    def anki_header(self):
        text = "Front\tBack\tExample\tOrigin\tUsage\t"
        text += "Part of speech\tSyllables\t"
        text += "Synonyms\tAntonyms\t"
        text += "Other usages\tPronunciation\tTags\n\n"
        return text



    def make_string(self):
        word = self
        entry = "{w.word}\t{w.definition}\t".format(w=word)
        entry += "{w.example}\t".format(w=word)
        entry += "{w.origin}\t".format(w=word)
        entry += "{w.part_of_speech}\t".format(w=word)
        entry += "{w.syllables}\t".format(w=word)
        entry += "{w.synonyms}\t".format(w=word)
        entry += "{w.antonyms}\t".format(w=word)
        entry += "{w.other_usages}\t".format(w=word)
        entry += "{w.pronunciation}\t".format(w=word)
        entry += "{w.tags}\n".format(w=word)
        entry += "\n"
        return entry

    def __str__(self):
        return self.word

    def time_ago(self):
        return naturaltime(self.timestamp)


class WordSearch(Model):
    searched_by = ForeignKey(User, blank=True, null=True)
    search = CharField(max_length=180, default="No Search Entry")
    words = ManyToManyField('Word', blank=True)
    times_searched = IntegerField(blank=True, null=True)
    timestamp = DateTimeField(
        editable=False, auto_now_add=True, auto_now=False)

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
    my_namespace = CharField(default="Venue", max_length=128, null=True, blank=True)
    tags = ManyToManyField(Tag, blank=True)

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
    my_namespace = CharField(default="Review", max_length=128, null=True, blank=True)

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

    def __str__(self):
        try:
            my_user = self.user.username
        except:
            my_user = "Null User"
        return '{} Submitted Image on {}'.format(my_user, self.timestamp)

    def time_ago(self):
        return naturaltime(self.timestamp)

    def __str__(self):
        try:
            return '{} Image {}'.format(self.venue.name, self.id)
        except:
            pass
        try:
            return '{} Menu {}'.format(self.venue.name, self.id)
        except:
            pass
        try:
            if not self.user_image:
                raise ValueError("No user picture")
            else:
                return '{} Profile'.format(self.user.username)
        except:
            pass
        return "no string"

def make_all_user_profiles():

    users = User.objects.all()

    for user in users:
        try:
            user.user_profile
        except:
            u = UserProfile(user=user)
            u.save()

        
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    profile_pic = models.ForeignKey('Image', null=True, blank=True, related_name='user_profile')
    all_profile_pics = models.ManyToManyField('Image', blank=True, related_name="user_profiles")

    def __str__(self):
        return '{} Profile'.format(self.user.username)


def create_user_profile(sender, **kwargs):
    """Creates a User Profile upon creation of User"""
    user = kwargs['instance']
    if kwargs['created']:
        user_profile = UserProfile(user=user)
        user_profile.save()



post_save.connect(create_user_profile, sender=User)