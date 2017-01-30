/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
/*TODO refactor for SSE */
(function display($, d) {
    var eventOutputContainer = document.getElementById("event");
    var evtSrc = new EventSource("/subscribe");

    evtSrc.onmessage = function(e) {
    console.log(e.data);
    eventOutputContainer.innerHTML = e.data;
    };
    socket.on('addTracks', function (Tracks) {
        JSON.parse(Tracks).forEach(addTrack);
    });

    socket.on('updateTrack', function (id, time, title, artist, group, rivendell, requester) {
        var row = $("tr#" + id.toString()).fadeOut();
        row.propertyIsEnumerable();
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
     * Adds tracks into the logger_body ID element - the body tag of the main table
     */
    function addTrackToTop(track) {
        console.log(track);
        $("<tr id='" + track.id + "' >" +
            "<td class='text-center'>" + track.artist + "</td>" +
            "<td  class='text-center'>" + track.title + "</td>" +
            "<td  class='text-center'>" + track.time + "</td>" +
            (detailed ?
            "<td  class='text-center'>" +
            ( track.rvdl ? "<a class='button tiny disabled round alert'>rvdl</a>" : "") +
            "</td>" +
            "<td  class='text-center'>" + track.group + "</td>" +
            "<td  class='text-center'>" + (track.requester ? track.requester : "" ) + "</td>" : "") +
            "</tr>").hide().insertAfter($("#column_headers")).fadeIn("slow");
    }
})(jQuery, detailed);
