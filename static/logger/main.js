/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
(function display($, d) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connected', function (tracks) {
        JSON.parse(tracks).forEach(addTrackToTop);
    });

    socket.on('addTracks', function (Tracks) {
        JSON.parse(Tracks).forEach(addTrack);
    });

    socket.on('updateTrack', function (id, time, title, artist, group, rivendell, requester) {
        var row = $("tr#" + id.toString()).fadeOut();
        row.propertyIsEnumerable()
    });

    socket.on('removeTrack', function (id) {
        $("#" + id.toString()).fadeOut().remove();
    });

    /* pagination: store date range client side and query */
    function nextRange() {
        socket.send();
        $("tr").fadeOut("fast").remove();
    }

    $("#Search").click(function () {
        socket.send('search', {'title': title, 'artist': artist, 'start': start.toString(), 'end': end.toString()});
    });

    /**
     * Adds tracks into the logger_body ID element, the body tag of the main table
     */
    function addTrackToTop(track) {
        console.log(track);
        $("<tr id='" + track.id + "' >" +
            "<td>" + track.artist + "</td>" +
            "<td>" + track.title + "</td>" +
            "<td>" + track.time + "</td>" +
            (detailed ?
            "<td>" +
            ( track.rvdl ? "<a class='button tiny disabled round alert'>rvdl</a>" : "") +
            "</td>" +
            "<td>" + track.group + "</td>" +
            "<td>" + (track.requester ? track.requester : "" ) + "</td>" : "") +
            "</tr>").hide().prependTo($("#logger_body")).fadeIn("slow");
    }
})(jQuery, detailed);
