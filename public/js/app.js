var app = {
   
   refreshResult: function(){
       var query = "";
       
       var value = $("#select-filter-country").val();
       
       if(value != ""){
           query += "country_code_k:" + value;
       }
       
       value = $("#select-filter-section").val();  
       if(value != ""){
           if(query != ""){ query += " AND "}
           query += "section_k:" + value;
       }
       
       value = $("#select-filter-subsection").val();
       if(value != ""){
           if(query != ""){ query += " AND "}
           query += "subsection_k:" + value;
       }
       
       value = $("#select-filter-nop").val();
       value = value.split(",");
       if(value[0] != "" && value.length > 1 && ( parseInt(value[0]) !== 0 || parseInt(value[1]) !== 100)){
           if(query != ""){ query += " AND "}
           query += "number_of_persons_involved_i:[" + value[0] + " to " +  value[1] + "]";
       }
       
       value = $("#select-filter-registration_date").val();
       value = value.split(",");
       if(value.length == 2 && ( parseFloat(value[0]) > 2008 || parseFloat(value[1]) < app.slide_date_to)){
           var year_from = Math.floor(parseFloat(value[0]));
           var month_from = 1 + Math.round(11 * (parseFloat(value[0]) - year_from));

           var year_to = Math.floor(parseFloat(value[1]));
           var month_to = 1 + Math.round(11 * (parseFloat(value[1]) - year_to));
            
           query += "registration_date_d:[" + year_from + "-" + month_from + " to " +   year_to + "-" + month_to  + "]";
       }
       
       value = $("#inp-filter-search").val();
       value = value.replace(/[^0-9a-zA-Z -]/gm, '')
       if(value != ""){
          
           var sub_query = ""; 
           
           $.each(value.split(" "), function(i, v){
               if(sub_query != ""){ sub_query += " AND "}
               v += "*";
               sub_query += "(organisation_name_s:" + v + " OR member_organisations_s:" + v + " OR goals__remit_s:" + v + ")";
           })
           
           if(query != ""){ query += " AND "}
           query += "(" + sub_query + ")"
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
        nopChart.draw(app.facets.number_of_persons, $('#chartSelect--nop :selected').val())
        registration_date_chart.draw(app.facets.registration_month, "bar")
   },
   
   loadList: function(res){
       $("#filter-res-count").html("[count] companies".replace("[count]", res.data.count) );
       app.loadMap(res.data.entities);
       app.loadTable(res.data.entities);
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
        
        $('#chartSelect--nop').change(function() {
            nopChart.draw(app.facets.number_of_persons, $(this).find(':selected').val())
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
        
        $("#select-filter-nop").slider({
            formatter: function(value) {
                    if(value.length !== 2){
                        return "";
                    }
                    $("#nop_from").text( value[0]);
                    $("#nop_to").text(value[1]);
                    
                    return value[0] + " to " +  value[1];
            }
        });
        $("#select-filter-nop").on("slideStop", app.refreshResult);
        
        app.slide_date_to = (new Date()).getFullYear() + 1;
        
        $("#select-filter-registration_date").slider({
            min: 2008,
            max: app.slide_date_to,
            step: 0.1,
            value: [2008, app.slide_date_to],
            formatter: function(value) {
                    if(value.length !== 2){
                        return "";
                    }
                    var year_from = Math.floor(value[0]);
                    var month_from = 1 + Math.round(11 * (value[0] - year_from));
                    
                    var year_to = Math.floor(value[1]);
                    var month_to = 1 + Math.round(11 * (value[1] - year_to));
                    
                    $("#registration_from").text(year_from + "-" + month_from);
                    $("#registration_to").text(year_to + "-" + month_to);
                    
                    return year_from + "-" + month_from + " to " + year_to + "-" + month_to;
            }
        });
        $("#select-filter-registration_date").on("slideStop", app.refreshResult);
        
        
        $("#form-filter").submit(function(e){ e.preventDefault(); app.refreshResult()});
        
        $(document).on("click", "a[data-identification_number]", app.onDetailsClick)
    },
    
    onDetailsClick: function(e){
       e.preventDefault();
       var identification_number = $(e.currentTarget).data("identification_number");
       console.log(identification_number);  
        
        $.ajax({
            method: 'POST',
            url: '/detail',
            data: JSON.stringify({"id": identification_number}),
        }).done(app.shopDetails);
        
    },
    
    shopDetails: function(info){
        console.log(info);
                
        $.each(info.data, function(k, v){
            if(v && v.replace){
                v = v.replace(/(?:\r\n|\r|\n)/g, '<br>')
            }
           $("[data-detail='" + k + "']").html(v);
        });

        $("#detail-modal").off("shown.bs.modal");
        $("#detail-modal").on("shown.bs.modal", function(){
            if (app.detailsmap){
                app.detailsmap.off();
                app.detailsmap.remove();
            }

            document.getElementById('details-map').innerHTML = "<div id='inner_detail_map' style='width: 100%; height: 300px;'></div>";
            var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
            }),
            latlng = L.latLng(info.data.lat, info.data.lon);

            app.detailsmap = L.map('inner_detail_map', {center: latlng, zoom: 4, layers: [tiles]});

            var markers = L.markerClusterGroup();

            var marker = L.marker(new L.LatLng(info.data.lat, info.data.lon), { title: info.data.organisation_name });
            //var content = "<a href='#' data-identification_number='" + entities[i].id + "'>" + entities[i].organisation_name + "</a>";
            //marker.bindPopup(content);
            markers.addLayer(marker);

            app.detailsmap.addLayer(markers);
        });
        
        $("#detail-modal").modal("show");
    },
    
    loadMap: function(entities) {
        if (app.map){
            app.map.off();
            app.map.remove();
        }
        document.getElementById('map').innerHTML = "<div id='inner_map' style='width: 100%; height: 100%;'></div>";
        var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
        }),
        latlng = L.latLng(51.144725, 12.226063);

        app.map = L.map('inner_map', {center: latlng, zoom: 5, layers: [tiles]});

        var markers = L.markerClusterGroup();

        for (var i = 0; i < entities.length; i++) {
            var marker = L.marker(new L.LatLng(entities[i].lat, entities[i].lon), { title: entities[i].organisation_name });
            var content = "<a href='#' data-identification_number='" + entities[i].id + "'>" + entities[i].organisation_name + "</a>";
            marker.bindPopup(content);
            markers.addLayer(marker);
        }

    app.map.addLayer(markers);
    },
    
    loadTable: function(entities){
        if (app.table){
            app.table.state.clear();
            app.table.destroy();
        } 
        
        app.table = $('#table').DataTable( {
                "processing": true,
                "serverSide": true,
                ajax: function(data, callback, settings){
                    
                    var order_column = data.order[0].column;
                    var order_dir = data.order[0].dir;
                    var search = data.search.value;
                    
                    var source = entities;

                    var sort_function = function(e1, e2) {
                            if (e1.organisation_name < e2.organisation_name) {
                                    return order_dir == "asc" ? -1 : 1;
                            }
                            return order_dir == "asc" ? 1 : -1;
                    };
                    
                    if(order_column == 1){
                        sort_function = function(e1, e2) {
                                return (e1.number_of_persons - e2.number_of_persons) * (order_dir == "asc" ? 1 : -1);
                        };
                    } 
                    else if(order_column == 2){
                        sort_function = function(e1, e2) {
                                if (e1.www < e2.www) {
                                        return order_dir == "asc" ? -1 : 1;
                                }
                                return order_dir == "asc" ? 1 : -1;
                        };
                    } 
                    else if(order_column == 3){
                        sort_function = function(e1, e2) {
                                if (dicts.countries[e1.country_code] < dicts.countries[e2.country_code]) {
                                        return order_dir == "asc" ? -1 : 1;
                                }
                                return order_dir == "asc" ? 1 : -1;
                        };
                    } 
                    
                    source.sort(sort_function);
                    
                    if(search != ""){
                        search = search.toLowerCase();
                        source = source.filter(function(e1){
                            return e1.organisation_name.toLowerCase().indexOf(search) > -1
                        });
                    }
                    
                    var rows = [];
                    var last_idx = data.start + data.length; 
                    if(last_idx > source.length) {
                        last_idx = source.length
                    }
                    
                    for(var i = data.start; i < last_idx; i++){
                        var obj = source[i];
                        
                        var website = "";
                        if(obj.www && obj.www){
                            website = "<a target='_blank' href='" + obj.www + "'>" + obj.www + "</a>";
                        }
                        
                        var name = "<a href='#' data-identification_number='" + obj.id + "'>" + obj.organisation_name + "</a>";
                        
                        rows.push([
                            name,
                            obj.number_of_persons,
                            website,
                            dicts.countries[obj.country_code]
                        ]);
                    }
                    
                    
                    callback({
                        draw: data.draw,
                        recordsFiltered: source.length,
                        recordsTotal: source.length,
                        data: rows
                    });
                }
            } );
    }
};
 
$(document).ready(function() {
    app.init();
});
