kr = {request_id: 0};

kr.on_mobile = function(){
    return (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i).test(navigator.userAgent);
};

kr.style = {
    if_missing_red: function(input){
        if (input === null || input === undefined || input === "unknown"){
            return '<em style="color: red">unknown</em>';
        } else {
            return input;
        }
    }
};

kr.session = {};

kr.session.has_zoom = function(){
    return sessionStorage !== undefined && sessionStorage.kr_zoom !== undefined;
};

kr.session.has_possition = function(){
    return sessionStorage !== undefined && sessionStorage.kr_lng !== undefined && sessionStorage.kr_lat !== undefined;
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

if (kr.on_mobile()) {
    kr.statistics.toggle();
}

kr.refresh_markers = function(bounds){
    bounds = bounds || kr.map.getBounds();

    $("#nav_status").html('<span class="label label-warning">Loading...</span>');
    kr.request_id++;

    var url = "/api/v1/places/?limit=500&in_bbox=" + bounds.toBBoxString() + "&request_id=" + kr.request_id;
    if (kr.on_mobile()){
        url = url + "&limit=100";
    }
    xhr = $.getJSON(url, function(response, status, xhr){
        $("#zoom_in_alert").hide();
        if (response.meta.request_id == kr.request_id) {
            kr.markers.clearLayers();
            for (var i in response.objects) {
                place = response.objects[i];

                var icon;
                if (place.religion in kr.marker_icons) {
                    icon = kr.marker_icons[place.religion];
                } else {
                    icon = kr.marker_icons['default'];
                }

                var marker = new L.marker([place.point.coordinates[1], place.point.coordinates[0]], {icon: icon});
                marker.place_id = place.id;
                marker.place_name = place.name;
                marker.place_religion = place.religion;
                marker.place_denomination = place.denomination;

                marker.on("click", kr.on_marker_click);
                marker.on("mouseover", kr.on_marker_mousehover);
                marker.addTo(kr.markers);
            }
            $("#nav_status").html('<span class="label label-success">'+ response.objects.length + ' places</span>');
            /*
            if (response.statistics.religion !== undefined) {
                var religions = [];
                for (var religion in response.statistics.religion) {
                    if (response.statistics.religion.hasOwnProperty(religion)) {
                        religions.push(religion);
                    }
                }
                religions.sort();
                if (religions.indexOf("unknown") !== -1) {
                    religions.pop("unknown");
                    religions.push("unknown");
                }

                var religion_statistic = "";
                for (var z=0; z<religions.length; z++) {
                    religion = religions[z];
                    var count = response.statistics.religion[religion];

                    if (religion === "unknown") {
                        religion_statistic += "<li style='color: red;'><em>" + religion + "</em>: <b>" + count + "</b></li>";
                    } else {
                        religion_statistic += "<li>" + religion + ": <b>" + count + "</b></li>";
                    }
                }
                $("#stats_ul").html('<li class="nav-header">Statistics</li><li class="active"><a href="#"><b>religion</b></a></li>' + religion_statistic);
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
            */
        }
    }).error(function(){
        if (xhr.status === 400) {
            $("#nav_status").html('<span class="label label-important"><strong>Please zoom in.</strong> There are to many places to display.</span>');
            kr.markers.clearLayers();
            if (kr.statistics.is_visible()){
                kr.statistics.hide(function(){
                    $("#stats_ul").html('<li class="nav-header">Statistics</li><li>There are no statistics about your map sector.</li>');
                });
            }
        }
    });
};

kr.run_geolocate = function(){
    kr.map.locate({setView: true, maxZoom: 16});
};

kr.on_marker_click = function(e){
   window.location = "/" + e.target.place_id;
};

kr.on_marker_mousehover = function(e){
    var placement = "top";
    if (e.originalEvent.layerY < 130) {
        placement = "bottom";
    }
    if (e.originalEvent.layerX < 150) {
        placement = "right";
    } else if ((kr.map._container.clientWidth - e.originalEvent.layerX) < 150) {
        placement = "left";
    }

    var content = "";
    content += "<p>religion: " + kr.style.if_missing_red(e.target.place_religion) + "<br/>";
    content += "denomination: " + kr.style.if_missing_red(e.target.place_denomination) + "</p>";

    $(e.target._icon).popover({
        animation: false,
        placement: placement,
        trigger: 'hover',
        html: true,
        title: "<strong>" + kr.style.if_missing_red(e.target.place_name) + "</strong>",
        content: content
    });
    $(e.target._icon).popover('show');
};

kr.buildMap = function(options){
    options = {
        target: options.target,
        center: options.center,
        zoom: options.zoom,
        use_session: options.use_session || false,
        locate: options.locate || false,
        allow_selection: options.allow_selection || false
    };

    if (options.use_session) {
        if (kr.session.has_possition()) {
            options.center = kr.session.get_possition();
        }
        if (kr.session.has_zoom()) {
            options.zoom = kr.session.get_zoom();
        }
    }

    var osm_layer = new L.TileLayer(
        'http://{s}.tile.cloudmade.com/3872B775BBB74188AAFBF300F25489EB/997/256/{z}/{x}/{y}.png',
        {
            minZoom: 3,
            maxZoom: 18,
            attribution: 'Map data © OpenStreetMap contributors, Imagery © CloudMade'
        }
    );
    kr.map = L.map(options.target, {
        csr: L.CRS.EPSG4326
    });
    kr.map.addLayer(osm_layer);
    kr.map.setView(options.center, options.zoom);

    // Base marker layer
    kr.markers = new L.LayerGroup();
    kr.markers.addTo(kr.map);

    kr.marker_icons = {
        'default': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/pin.png',
            iconSize: [15, 24]
        }),
        'christian': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/christianity_church.png',
            iconSize: [24, 25]
        }),
        'islam': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/islam.png',
            iconSize: [25, 24]
        }),
        'muslim': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/islam.png',
            iconSize: [25, 24]
        }),
        'hindu': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/hindu.png',
            iconSize: [24, 24]
        }),
        'budddhist': L.icon({
            iconUrl: STATIC_URL + 'lib/kirchenreich/icons/buddhist.png',
            iconSize: [28, 22]
        })
    };

    // Geolocation
    if (options.locate) {
        kr.map.locate();
    }

    // Selection
    if (!kr.on_mobile() && options.allow_selection) {
        kr.locationSelection = new L.LocationFilter().addTo(kr.map);
        var button = $("div.location-filter a");
        button.text("");

        kr.locationSelection.on("change", function (e) {
            kr.refresh_markers(e.bounds);
        });
        kr.locationSelection.on("enabled", function (e) {
            kr.refresh_markers(kr.locationSelection.getBounds());
        });
        kr.locationSelection.on("disabled", function () {
            button.text("");
            kr.refresh_markers();
        });
    }

    kr.map.on('moveend', function() {
        if (kr.locationSelection !== undefined && kr.locationSelection.isEnabled()) {
            return null;
        }

        kr.refresh_markers();
        if (options.use_session && sessionStorage) {
            kr.session.set_possition(kr.map.getCenter());
            kr.session.set_zoom(kr.map.getZoom());
        }
    });

    kr.refresh_markers();

    if (options.use_session && (kr.session.has_possition() || kr.session.has_zoom())) {
        kr.refresh_markers();
    }

};
