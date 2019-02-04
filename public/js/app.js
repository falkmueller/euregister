var app = {
    loadData: function(query){
        query = query || "*:*"
        
        console.log("search: " + query);
        
        return $.ajax({
            method: 'POST',
            url: '/search',
            data: JSON.stringify({"query": query, page: 1, pagelen: 100000}),
        });
   },
   
   refreshResult: function(){
       var query = "";
       
       var country = $("#select-filter-country").val();
       
       if(country != ""){
           query = "country_code_k:" + country;
       }
      
       app.loadData(query).done(app.loadResult);
   },
   
   loadResult: function(res) {
       // any previous charts need to be cleared away first
        clearChart(app);
        app.chart = drawDoughnutChart(res.data.facets.countries);
        app.countryData = res.data.facets.countries;
        if ($('#chartSelect :selected').val() === "bar") {
            app.chart = drawBarChart(app.countryData);
        } else {
            app.chart = drawDoughnutChart(app.countryData);
        }
        console.log(res);
        app.loadMap(res.data.entities);
   },
   
   init: function(){
        app.loadData().done(app.loadResult).done(function(res){
            $("#count").text(res.data.count);
            
            var ddlCountry = $("#select-filter-country");
            $.each(res.data.facets.countries, function(k, v){
                ddlCountry.append(new Option(v.name, k));
            });
            
        });
        
        $('#chartSelect').change(function() {
            clearChart(app);
            if ($(this).find(':selected').val() === "bar") {
              app.chart = drawBarChart(app.countryData);
            } else {
              app.chart = drawDoughnutChart(app.countryData);
            }
        });
        
        $("#select-filter-country").change(app.refreshResult);
    },
    
    loadMap: function(entities) {
        if (app.map){
            app.map.off();
            app.map.remove();
        }
        document.getElementById('map').innerHTML = "<div id='map' style='width: 100%; height: 100%;'></div>";
        var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
        }),
        latlng = L.latLng(51.144725, 12.226063);

        app.map = L.map('map', {center: latlng, zoom: 5, layers: [tiles]});

        var markers = L.markerClusterGroup();

        for (var i = 0; i < entities.length; i++) {
            var marker = L.marker(new L.LatLng(entities[i].lat, entities[i].lon), { title: entities[i].organisation_name });
            marker.bindPopup(entities[i].organisation_name);
            markers.addLayer(marker);
        }

    app.map.addLayer(markers);
    }
};
 
$(document).ready(function() {
    app.init();
});
