from . forms import UserLoginForm, CreateUserForm, UserImageForm


from . models import SchoolClass

def school_classes_processor(request):
    school_classes = SchoolClass.objects.all()
    context = {'school_classes': school_classes}

    return context

def forms_processor(request):
    context = {'user_login_form': UserLoginForm(), 
               'create_user_form': CreateUserForm(),
               'user_image_form': UserImageForm()}
    return context



def current_time_processor(request):
    # DONT FOR GET TO ADD
    # THESE TWO LINES TO YOUR settings.py!!
    # TEMPLATE_CONTEXT_PROCESSORS += ("auto_dict.context_processors.current_time_processor", )
    # TEMPLATES[0]['OPTIONS']['context_processors'].append("auto_dict.context_processors.current_time_processor")
    from datetime import datetime
    d = datetime.now()
    current_time_string = d.strftime("%I:%M%p %A %B %d, %Y")
    current_time = d
    return {'current_time': current_time,
            'current_time_string': current_time_string}
