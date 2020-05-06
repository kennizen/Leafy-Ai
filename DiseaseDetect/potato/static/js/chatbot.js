var $messages = $('.messages-content');
var serverResponse = 'wala';

var suggession;
//speech reco
try {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
} catch (e) {
    console.error(e);
    $('.no-browser-support').show();
}

$('#start-record-btn').on('click', function (e) {
    recognition.start();
});

recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    document.getElementById('MSG').value = speechToText;
    //console.log(speechToText)
    insertMessage();
};

function listendom(no) {
    console.log(no);
    //console.log(document.getElementById(no))
    document.getElementById('MSG').value = no.innerHTML;
    insertMessage();
}

$(window).load(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
        serverMessage('Hi! I am Leafy Bot. I am here to answer your questions. How can i help you ?');
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar('update').mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0,
    });
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '<figure class="user-avatar"><img src='+human+'></figure></div>').appendTo($('.mCSB_container')).addClass('new');
    // fetchmsg()

    $('.message-input').val(null);
    updateScrollbar();
}

document.getElementById('mymsg').onsubmit = (e) => {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/chat/',
        data: {
            query: $('.message-input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            insertMessage();
            serverMessage(data.replyy);
        },
    });
};

function serverMessage(response2) {
    if ($('.message-input').val() != '') {
        return false;
    }
    $(
        '<div class="message loading new"><figure class="avatar"><img src=' +
            bot +
            '/></figure><span></span></div>'
    ).appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        $('.message.loading').remove();
        $(
            '<div class="message new"><figure class="avatar"><img src=' +
                bot +
                '/></figure>' +
                response2 +
                '</div>'
        )
            .appendTo($('.mCSB_container'))
            .addClass('new');
        updateScrollbar();
    }, 100 + Math.random() * 20 * 100);
}
