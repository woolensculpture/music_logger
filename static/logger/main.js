/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
(function display($) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('search', p);
    });
    socket.on('addTracks', function (Tracks) {
        Tracks.forEach(addTrack);
    });

    socket.on('updateTrack', function (id, time, title, artist, group, rivendell, requester) {
        $("#" + id.toString());
    });

    socket.on('removeTrack', function (id) {
        $("#" + id.toString()).fadeOut().remove();
    });

    /* pagination: store date range client side and query */
    function nextRange() {
        socket.send();
        $(".row[id!=header]").remove();
    }

    function search(id, time, title, artist, group, rivendell, requester) {

    }

    function addTrack(id, time, artist, title) {
        $("div#header").insertAfter("<div id='" + id + "' class='row'><div class='column'>" + time +
            "</div><div class='column'>" + artist + "</div><div class='column'>" + title + "</div></div>");
    }

    b
})(jQuery);
