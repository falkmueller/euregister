var app = {
   
   refreshResult: function(){
       var query = "";
       
       var value = $("#select-filter-country").val();
       
       if(value != ""){
           query += "country_code_k:" + value;
       }
       
       var value = $("#select-filter-section").val();
       
       if(value != ""){
           if(query != ""){ query += " AND "}
           query += "section_k:" + value;
       }
       
       var value = $("#select-filter-subsection").val();
       
       if(value != ""){
           if(query != ""){ query += " AND "}
           query += "subsection_k:" + value;
       }
       
       query = query || "*:*";
       
       $.ajax({
            method: 'POST',
            url: '/facets',
            data: JSON.stringify({"query": query}),
        }).done(app.loadFacets);
        
        $.ajax({
            method: 'POST',
            url: '/list',
            data: JSON.stringify({"query": query, page: 1, pagelen: 100000}),
        }).done(app.loadList);
   },
   
   loadFacets: function(res) {
        app.facets = res.data;
        countryChart.draw(app.facets.countries, $('#chartSelect :selected').val())
        sectionChart.draw(app.facets.sections, app.facets.subsections, $('#chartSelect--sections :selected').val())
   },
   
   loadList: function(res){
       app.loadMap(res.data.entities);
   },
   
   init: function(){
        $("#count").text(dicts.count);
        
       var ddlCountry = $("#select-filter-country");
       var keysSorted = Object.keys(dicts.countries).sort(function(a,b){
            var x = dicts.countries[a].toLowerCase();
            var y = dicts.countries[b].toLowerCase();
            return x < y ? -1 : x > y ? 1 : 0;
       })
        $.each(keysSorted, function(k, v){
            ddlCountry.append(new Option(dicts.countries[v], v));
        });
        
        var ddlSection = $("#select-filter-section");
       var keysSorted = Object.keys(dicts.sections).sort(function(a,b){
            var x = dicts.sections[a].name.toLowerCase();
            var y = dicts.sections[b].name.toLowerCase();
            return x < y ? -1 : x > y ? 1 : 0;
       })
        $.each(keysSorted, function(k, v){
            ddlSection.append(new Option(dicts.sections[v].name, v));
        });
            
        app.refreshResult();
        
        $('#chartSelect').change(function() {
            countryChart.draw(app.facets.countries, $(this).find(':selected').val())
        });
        
        $('#chartSelect--sections').change(function() {
            sectionChart.draw(app.facets.sections, app.facets.subsections, $(this).find(':selected').val())
        });
        
        $("#select-filter-country").change(app.refreshResult);
        $("#select-filter-section").change(app.refreshResult).change(function(){
            var section = $(this).val();
            var subSelect = $("#select-filter-subsection");
            $("option[value!='']", subSelect).remove();
            if(section != ""){
                $.each(dicts.sections[section].subsections, function(subsection, val){
                      var option = $("<option />");
                      option.html(val.name);
                      option.attr("value", subsection);
                      subSelect.append(option);
                });
            }
        });
        
        $("#select-filter-subsection").change(app.refreshResult);
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
