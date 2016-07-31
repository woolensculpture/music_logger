/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
(function display($) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('search',);
    });
    socket.on('newTrack', function (time, title, artist, group, requester) {

    });

    socket.on('updateTrack', function () {

    });

    socket.on('removeTrack', function (id) {
        $(".row#" + id).remove();
    });

    /* next page */
    function nextRange() {
        socket.send();
        $(".row[id!=header]").remove();
    }

    function search() {

    }

    function addTrack(id, time, artist, title) {
        $("div#header").insertAfter("<div id='" + id + "' class='row'><div class='column'>" + time +
            "</div><div class='column'>" + artist + "</div><div class='column'>" + title + "</div></div>");
    }

    function updateTrack(id, time, artist, title) {
        $("div#id");
    }

})(jQuery);
