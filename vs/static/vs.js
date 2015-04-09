function anyinput(event) {
    if (event.keyCode == 13) {
        submit();
    }

    var rc = $('.result-container');
    if (rc.css('opacity') > 0) {
        rc.animate({opacity: 0.0});
    }
    $('#error').text('');
}


function _submitDone(data) {
    console.log(data);

    $('.result-container').animate({opacity: 1.0});
    $('#result').val(data.url).select();
    $('#submit').html('Shorten').click(submit);
}

function _apiError(xhr) {
    console.log(xhr);
    data = JSON.parse(xhr.responseText);

    $('#error').text(data.message);
    $('#submit').html('Shorten').click(submit);
}

function submit() {
    data = {url: $('#url').val()};
    var id = $('#id').val().trim();
    if (id.length > 0) {
        data.id = id;
    }

    $.ajax({
        async: true,
        type: 'PUT',
        dataType: 'json',
        url: 'api/v1/short',
        success: _submitDone,
        error: _apiError,
        data: data
    });

    $('#submit').html('Shortening <i class="fa fa-spinner fa-pulse"></i>').unbind('click');
}

function _useConfig(data) {
    $('#id').removeAttr('disabled');
    if(!data.custom_ids) {
        $('#id').attr('disabled', 'disabled');
    }

    $('#id').unbind('keypress').keypress(function(event) {
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (data.alphabet.indexOf(key) == -1) {
            event.preventDefault();
            return false;
        }
    })
}

function useConfig() {
    $.ajax({
        async: true,
        type: 'GET',
        dataType: 'json',
        url: 'api/v1/domain',
        success: _useConfig
    });
}


$(document).ready(function() {
    $('#error aside').remove();
    useConfig();

    // submit on enter
    $('#url').keyup(anyinput).focus();
    $('#id').keyup(anyinput);

    $('#submit').click(submit)
})