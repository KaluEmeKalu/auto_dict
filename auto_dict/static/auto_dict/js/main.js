// This loads date picker .and calendar image
$( function() {
    $( ".datepicker" ).datepicker({
        showOn: "button",
        buttonImage: $('.calendar_image_url').attr('value'),//"{% static 'portals/images/calendar.png' %}",
        buttonImageOnly: true,
        buttonText: "Select date"
    });
    $( ".datepicker" ).datepicker( "option", "dateFormat", "DD" );
});//end date picker calendar image.

$('.basicExample').timepicker();

// When Date Picker Changes Show Date Selected
    $('#datepicker').change(function() {
        $( ".spanDate" ).html($( "#datepicker" ).val() + 's');
    })//end change

    $('#datepicker2').change(function() {
        $( ".spanDate2" ).html($( "#datepicker2" ).val() + 's');
    })//end change

    $('#datepicker3').change(function() {
        $( ".spanDate3" ).html($( "#datepicker3" ).val() + 's');
    })
// When Date Picker Changes Show Date Selected End

function Register() {
    $('.ajaxProgress').show();
    $.ajax({
        type: "POST",
        url: $('.register_form input.url').val(),
        dataType: "json",
        async: true,
        data: {
            csrfmiddlewaretoken: $('.register_form input[name=csrfmiddlewaretoken]').val(),
            username: $('#id_username').val(),
            email: $('#id_email').val(),
            password: $('#id_password').val(),
        },//data close

        success: function(json) {
            console.log(json.message, json.username, json.password);
            $('ajaxProgress').hide();
            $('.register_form').toggle('');
            $('.student_form').toggle('');
        }


    })//ajax close
}//function Register close

    console.log($('.student_form input[name=csrfmiddlewaretoken]').val())

function CreateStudent() {
    $('.ajaxProgress').show();
    $.ajax({
        type: "POST",
        url: $('.student_form input.url').val(),
        dataType: "json",
        async: true,
        data: {
            csrfmiddlewaretoken: $('.student_form input[name=csrfmiddlewaretoken]').val(),
            name: $('#id_name').val(),
            is_adult: $('input[name=is_adult]:checked').val(),
            age: $('#id_age').val(),
        },//data close

        success: function(json) {
            console.log( json.name, json.username, json.result);
            $('ajaxProgress').hide();
            $('.student_form').toggle('');
            $('.class_form').toggle('');
        }


    })//ajax close
}//function Register close

function CreateClass() {
    $('.ajaxProgress').show();
    $.ajax({
        type: "POST",
        url: $('.class_form input.url').val(),
        dataType: "json",
        async: true,
        data: {
            csrfmiddlewaretoken: $('.class_form input[name=csrfmiddlewaretoken]').val(),
            days_a_week: $('input[name=days_of_class]:checked').val(),
            
            day1: $('#datepicker').val(),
            day1_from: $('#timepicker1_from').val(),
            day1_to: $('#timepicker1_to').val(),

            day2: $('#datepicker2').val(),
            day2_from: $('#timepicker2_from').val(),
            day2_to: $('#timepicker2_to').val(),

            day3: $('#datepicker3').val(),
            day3_from: $('#timepicker3_from').val(),
            day3_to: $('#timepicker3_to').val(),

        },//data close

        success: function(json) {
            console.log(json.age, json.name, json.is_adult);
            $('ajaxProgress').hide();
            $('.register_form').toggle('');
            $('.student_form').toggle('');
            window.location.replace("http://127.0.0.1:8000/portals/");

        }


    })//ajax close
}//function Create Class close

// changes age visibility on is_adult change
$('.age_input input').change(function() {
    if ($(this).attr('id') === 'under_18') {
        $('#id_age').removeClass('age_hidden')
    } else {
        $('#id_age').addClass('age_hidden');
        $('#id_age').val('');
    }
})//end change

// changes calendar visibility days change
$('.days_of_class input').change(function() {
    if ($(this).attr('id') === '1day') {
    	$('.day1').show('')
        $('.day2').hide('')
        $('.day3').hide('')
    } else if ($(this).attr('id') === '2days') {
    	$('.day1').show('')
    	$('.day2').show('')
        $('.day3').hide('')
    }

    else {
        $('.day1').show('')
    	$('.day2').show('')
        $('.day3').show('')
    }
})//end change

// On Click Load Login
function loadLogin() {
    $( "#loadLogin .modal-body" ).load( "login/");
};


// On Click Load Register
function loadRegister() {
    $( "#loadRegister .modal-body" ).load( "register/");
};

// On Click Load Register
function loadChangeUserPic() {
    $( "#load_change_user_pic .modal-body" ).load( "change_user_image/");
};