/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
/*TODO refactor for SSE */
"use strict";
(function display($, detailed) {

    var eventOutputContainer = document.getElementById("event");
    var evtSrc = new EventSource("/subscribe");
    evtSrc.onmessage = function(e) {
        // TODO finish logic for adding, removing, and updating tracks.
        console.log(e.data);
        var msg = JSON.parse(e.data);
        switch(msg.action){
            case 'add':
                break;
            case 'prepend':
                break;
            case 'delete':
                removeTrack(msg.data);
                break;
            case 'update':
                break;
            default:
                console.error("ERROR: unknown action")
        }
    };

   function Track(artist, title, time, rvdl, requester, id){
        this.artist = artist;
        this.time = Date.parse(time);
        this.id = id;
        this.rvdl = rvdl;
        this.requester = requester ? requester : "";

        this.createHTML = function(){
            var trackHTML = "<tr id='" + this.id + "' class='track' >" +
                "<td class='artist'>" + this.artist + "</td>" +
                "<td  class='title'>" + this.title + "</td>" +
                "<td  class='time'>" + this.time + "</td>";
            if (detailed)
                trackHTML += "<td  class='rvdl'>" +
                    (this.rvdl ? "<a class='button tiny disabled round alert'>rvdl</a>" : "") +
                    "</td>" +
                    "<td  class='requester'>" + this.requester + "</td>";
            trackHTML += "</tr>";
            return trackHTML;
        };

        this.getTrackClass = function(){
            if(detailed && this.group != 'Library') {
                if(this.group.name == 'Feature')
                    return "table-feature";
                else if(this.group == 'New Bin')
                    return "table-newbin";
            }else {
                return "table-library";
            }
        };

    }

    function prependTrack(track){
        var trackHTML = $(createHTML(track));
        trackHTML.hide();
        $("#logger_body").prepend(trackHTML);
        trackHTML.fadeIn("fast");
    }
    function addTracks(Tracks) {
        //TODO finish
    }

    function updateTrack(id, time, title, artist, group, rivendell, requester) {
        //TODO finish
        var row = $("tr#" + id.toString()).fadeOut();
    }

    function removeTrack(id) {
        $("#" + id.toString()).fadeOut().remove();
    }

    /* pagination: store date range client side and query */
    function range(page) {
        //TODO finish
    }

    function search() {
        $.ajax(window.location.hostname + "/search", {
            start:$("td#startDate").val(),
            end:$("td#endDate").val(),
            artist:$('artistInput'),
            title:$('titleInput')
        });
        $(".track").fadeOut("fast").remove();
    }


    return {
        addTrack: addTracks,
        updateTrack: updateTrack,
        removeTrack: removeTrack,
        search: search,
        getPage: range
    };
})(jQuery, detailed);
