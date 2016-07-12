/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
(function display($) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('search',);
    });
    socket.on('newTrack', function () {

    });

    socket.on('updateTrack', function () {

    });

    socket.on('removeTrack', function (id) {
        $(id).remove();
    });

    socket.on('nextPage', function () {

    });

    socket.send("search")

    function addTrack()

    ()
    {

    }
    ;

})(jQuery);
