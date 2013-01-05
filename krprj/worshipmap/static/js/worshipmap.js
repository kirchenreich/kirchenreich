kr = {request_id: 0};

kr.session = {};

kr.session.has_zoom = function(){
    return sessionStorage && sessionStorage.kr_zoom;
};

kr.session.has_possition = function(){
    return sessionStorage && sessionStorage.kr_lng && sessionStorage.kr_lat;
};

kr.session.get_possition = function(){
    return new L.LatLng(sessionStorage.kr_lat, sessionStorage.kr_lng);
};

kr.session.set_possition = function(possition){
    sessionStorage.kr_lng = possition.lng;
    sessionStorage.kr_lat = possition.lat;
};

kr.session.set_zoom = function(zoom){
    sessionStorage.kr_zoom = zoom;
};

kr.session.get_zoom = function(){
    return sessionStorage.kr_zoom;
};

kr.statistics = {};
kr.statistics.toggle_show = true;
kr.statistics.is_visible = function(){
    return $("#stats_ul").is(":visible");
};

kr.statistics.toggle = function(){
    if (kr.statistics.is_visible()) {
        kr.statistics.hide();
        kr.statistics.toggle_show = false;
    } else {
        kr.statistics.show();
        kr.statistics.toggle_show = true;
    }
};

kr.statistics.show = function(callback){
    $("div#stats").fadeIn(callback);
    $("a#togglestats").text("Hide statistics");
};

kr.statistics.hide = function(callback){
    $("div#stats").fadeOut(callback);
    $("a#togglestats").text("Show statistics");
};

kr.refresh_markers = function(){
    $("#nav_status").html('<span class="label label-warning">Loading...</span>');
    kr.request_id++;
    xhr = $.getJSON("/api/v1/places/?epsg=4326&in_bbox=" + kr.map.getBounds().toBBoxString() + "&request_id=" + kr.request_id, function(response, status, xhr){
        $("#zoom_in_alert").hide();
        if (response.request_id == kr.request_id) {
            kr.markers.clearLayers();
            for (var i in response.places_of_worship) {
                place = response.places_of_worship[i];

                var icon;
                if (place.religion in kr.marker_icons) {
                    icon = kr.marker_icons[place.religion];
                } else {
                    icon = kr.marker_icons['default'];
                }

                marker = new L.marker([place.lat, place.lon], {icon: icon, title: "Hello World!"});
                marker.place_id = place.id;

                /*$(marker._icon).tooltip({
                   'title': place.name || "unknow" + "(" + place.religion || "unknow" + ")"
                }); */

                marker.on("click", kr.on_marker_click);
                marker.on("mouseover", function(){
                    alert("Hello");
                });
                marker.addTo(kr.markers);
            }
            $("#nav_status").html('<span class="label label-success">'+ response.places_of_worship_count + ' places</span>');
            if (response.statistics.religion !== undefined) {
                var religion = $.map(response.statistics.religion,
                    function(key, value) {
                        return "<li>" + value + ": <b>" + key + "</b></li>";
                    }
                );
                $("#stats_ul").html('<li class="nav-header">Statistics</li><li class="active"><a href="#"><b>religion</b></a></li>' + religion.join(""));
                if (!kr.statistics.is_visible() && kr.statistics.toggle_show) {
                    kr.statistics.show();
                }
            } else {
                if (kr.statistics.is_visible()){
                    kr.statistics.hide(function(){
                        $("#stats_ul").html('<li class="nav-header">Statistics</li><li>There are no statistics about your map sector.</li>');
                    });
                }
            }
        }
    }).error(function(){
        if (xhr.status == 422) {
            $("#nav_status").html('<span class="label label-important"><strong>Please zoom in.</strong> There are to many places of worship to display.</span>');
            kr.markers.clearLayers();
        }
    });
};

kr.run_geolocate = function(){
    kr.map.locate({setView: true, maxZoom: 16});
};

kr.on_marker_click = function(e){
   window.location = "/" + e.target.place_id;
};

kr.buildMap = function(target_div, center, zoom, use_session){
    if (use_session) {
        if (kr.session.has_possition()) {
            center = kr.session.get_possition();
        }
        if (kr.session.has_zoom()) {
            zoom = kr.session.get_zoom();
        }
    }

    var osm_layer = new L.TileLayer(
        'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            minZoom: 8,
            maxZoom: 18,
            attribution: 'Map data © OpenStreetMap contributors'
        }
    );
    kr.map = L.map(target_div, {
        csr: L.CRS.EPSG4326
    });
    kr.map.addLayer(osm_layer);
    kr.map.setView(center, zoom);

    // Base marker layer
    kr.markers = new L.LayerGroup();
    kr.markers.addTo(kr.map);

    kr.marker_icons = {
        'default': L.icon({
            iconUrl: STATIC_URL + 'icons/pin.png',
            iconSize: [15, 24]
        }),
        'christian': L.icon({
            iconUrl: STATIC_URL + 'icons/christianity_church.png',
            iconSize: [24, 25]
        }),
        'islam': L.icon({
            iconUrl: STATIC_URL + 'icons/islam.png',
            iconSize: [25, 24]
        }),
        'muslim': L.icon({
            iconUrl: STATIC_URL + 'icons/islam.png',
            iconSize: [25, 24]
        }),
        'hindu': L.icon({
            iconUrl: STATIC_URL + 'icons/hindu.png',
            iconSize: [24, 24]
        }),
        'budddhist': L.icon({
            iconUrl: STATIC_URL + 'icons/buddhist.png',
            iconSize: [28, 22]
        })
    };

    // Geolocation
    kr.map.locate();


    kr.map.on('moveend', function() {
        kr.refresh_markers();
        if (use_session && sessionStorage) {
            kr.session.set_possition(kr.map.getCenter());
            kr.session.set_zoom(kr.map.getZoom());
        }
    });

    kr.refresh_markers();

    if (use_session && (kr.session.has_possition() || kr.session.has_zoom())) {
        kr.refresh_markers();
    }

};
