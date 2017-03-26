from django.contrib import admin
from .models import (
    Venue,
    Address,
    Review,
    UserProfile,
    Image,
    WordSearch,
    Word)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_1', 'address_2', 'city', 'state', 'zip_code',
                    'country', 'area_of_city',)


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description', 'average_cost',
                    'delivery_available',
                    'pick_up_available', 'is_banned', 'timestamp', 'id',
                    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('comment', 'rating', 'is_banned', 'timestamp', 'venue')


class UserImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'user')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('my_namespace', 'user_image', 'user',
                    'venue_image', 'venue', 'menu_image')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic', 'can_add_venue', 'is_banned')


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'full_json_response', 'definition', 'timestamp')


class WordSearchAdmin(admin.ModelAdmin):
    list_display = ('search', 'timestamp')

admin.site.register(Venue, VenueAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(WordSearch, WordSearchAdmin)
admin.site.register(Word, WordAdmin)
