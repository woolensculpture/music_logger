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
