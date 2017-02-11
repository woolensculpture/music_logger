/**
 * Created by Benjamin Reynolds on 5/1/2016.
 */
/*TODO refactor for SSE */
"use strict";
var display = (function ($, detailed) {

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
                console.error("ERROR: unknown action");
                break;
        }
    };

    function Track() {
        if(arguments.length == 7) {
            //just pass in the parameters
            this.id = arguments[0];
            this.artist = arguments[1];
            this.time = new Date(arguments[2]);
            this.rvdl = !!(arguments[3]);
            this.title = arguments[4];
            this.requester = arguments[5];
            this.group = arguments[6];
            this.element = this.toHTML();
        }
        else if(arguments.length == 1)
            if (typeof arguments[0] === 'object') {

            }
            else if(typeof  arguments[0] === 'string'){
            // pass in raw json
            }
    }

    Track.prototype.parseFromHTML = function (trackRow) {
        this.element = trackRow;
        this.id =this.getField('id');
        this.artist = this.getField('artist');
        this.time = new Date(this.getField('time'));
        this.rvdl = !!(this.getField('rvdl'));
        this.title = this.getField('title');
        this.requester = this.getField('requester');
        this.group = this.getField('group');
        return this;
    };


    Track.FromJSON = function(json){
        // TODO probably rebinding the parsed JSON to the Track object is faster and more efficient,
        // just not confident enough with js to test that it works right now

        var fields = JSON.parse(json);
        this.toHTML(fields.id, fields.artist, fields.title, fields.time, fields.group, fields.rvdl, fields.requester);
        return this;
    };

    Track.prototype.toHTML = function(){
        var trackHTML = "<tr id='" + this.id + "' class='track " + detailed ? this.getTrackClass():"" + "' >" +
            "<td class='artist'>" + this.artist + "</td>" +
            "<td  class='title'>" + this.title + "</td>" +
            "<td  class='time'>" + this.time + "</td>";
        if (detailed)
            trackHTML +=
                "<td class='group'>" + this.group + "</td>" +
                "<td  class='rvdl'>" +
                (this.rvdl ? "<a class='button tiny disabled round alert'>rvdl</a>" : "") +
                "</td>" +
                "<td  class='requester'>" + this.requester + "</td>";
        trackHTML += "</tr>";
        this.element = $.parseHTML(trackHTML);
        return this;
    };

    Track.prototype.toJSON = function(){
        return JSON.stringify(
            {
                artist:this.artist,
                time:this.time.toString(),
                rvdl:this.rvdl,
                title:this.title,
                group:this.group
            });
    };

    Track.prototype.getTrackClass = function(){
        if(detailed && this.group != 'Library') {
            if(this.group.name == 'Feature')
                return "table-feature";
            else if(this.group == 'New Bin')
                return "table-newbin";
        }else {
            return "table-library";
        }
    };

    Track.prototype.getField = function(field) {
        if(field === 'id') return this.element.id;
        field = this.element.find("td." + field);
        return field.length > 0 ? field[0].innerText : '';
    };

    Track.prototype.setField = function(field, value) {
        field = this.element.find("td." + field);
        if(field.length > 0)
            field[0].innerText = !!(value) ? value : '';
        return this;
    };

    var TrackList = {
        element: $('#logger_body'),
        arr : $('#logger_body').find('tr').each(function(i,track){return (new Track()).parseFromHTML($(track))}),
        //TODO
        add: function(){},
        remove: function(){},
        append: function(){},
        sort: function(){},
        contains: function(){},
        find: function(){},
        foreach: function () {},
        filter: function () {}

    };

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
            start: $("td#startDate").val(),
            end: $("td#endDate").val(),
            artist: $('artistInput'),
            title: $('titleInput')
        });
        $(".track").fadeOut("fast").remove();
    }

    return {
        Track: Track,
        TrackList: TrackList,
        addTrack: addTracks,
        updateTrack: updateTrack,
        removeTrack: removeTrack,
        search: search,
        getPage: range
    };
}(jQuery, detailed));
