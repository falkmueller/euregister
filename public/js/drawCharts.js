function getRandomColor() {
    return "rgba(" + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ", 0.8)"
}

var customChart = {
    
    chart: null,
    
    title: "",
    
    selectors: {
        bar: "",
        doughnut: ""
    },
    
    draw: function(values, type){
        this.clearChart();
       
        if(type !== "bar"){
            this.chart = this.drawDoughnutChart(this.prepareData(values));
        } else {
            this.chart = this.drawBarChart(this.prepareData(values)); 
        }
    },
    
    clearChart: function() {
        if(!this.chart){
            return;
        }
        
        // remove and re-add the canvas element to wipe all lingering event handlers
        var clonedCanvas = this.chart.canvas.cloneNode();
        var nextSibling = this.chart.canvas.nextSibling;
        var parent = this.chart.canvas.parentNode;
        this.chart.canvas.remove();
        this.chart.destroy();
        parent.insertBefore(clonedCanvas, nextSibling);

        this.chart = null;
    },
    
    prepareData: function(rawValues) {
        return rawValues;
    },
    
    
    drawDoughnutChart: function(data) {
        $(this.selectors.bar).hide();
        $(this.selectors.doughnut).show();
        $(this.selectors.doughnut).height(500 + data.data.length * 2);
        
        var ctx = document.getElementById($(this.selectors.doughnut).attr("id"));
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: data.data,
                    backgroundColor: data.colors,
                    label: 'Registered companies'
                }],
                labels: data.labels
            },
            options: {
                responsive: true,
                cutoutPercentage: 20,
                maintainAspectRatio: false,
                legend: {
                    display: true,
                    position: "bottom",
                    labels: {
                        fontSize: 10
                    }
                },
                title: {
                    display: this.title != "",
                    text: this.title
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });

        return myChart;
    },

    drawBarChart: function(data) {
        $(this.selectors.doughnut).hide();
        $(this.selectors.bar).show();
        $(this.selectors.bar).height(100 + data.data.length * 12);
        $(this.selectors.bar).css({"max-width": "100%"});
         
        var ctx = document.getElementById($(this.selectors.bar).attr("id"));
        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                datasets: [{
                    data: data.data,
                    backgroundColor: data.colors,
                    label: 'Registered companies'
                }],
                labels: data.labels
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                title: {
                    display: this.title != "",
                    text: this.title
                },
                animation: {
                    animateScale: true,
                },
                scales: {
                    xAxes: [{
                        position: "top",
                        id: "x1",
                    }],
                    yAxes: [{
                        position: "left",
                        categoryPercentage: 0.8
                    }]
                }   
            }
        });
        return myChart;
    }
    
};






var sectionChart = $.extend({}, customChart, {
    selectors: { bar: "#chart_bar--sections", doughnut: "#chart_doughnut--sections"},
    draw: function(values, subvalues, type){
        this.clearChart();
        
        if(type !== "bar"){
            this.chart = this.drawDoughnutChart(this.prepareData(values));
        } else {
            this.chart = this.drawBarChart(this.prepareData(values, subvalues)); 
        }
    },
    prepareData: function(rawValues, subvalues) {
        var sortedValues = Object.keys(rawValues).map((id) => [id, rawValues[id], dicts.sections[id].name]);
        sortedValues.sort((i1, i2) => i2[1] - i1[1]);
        
        subvalues = subvalues || {};

        var preparedData = {
            labels: [],
            data: [],
            colors: []
        };
        $.each(sortedValues, function(i, v){
           preparedData.labels.push(v[2]);
           preparedData.data.push(v[1]);
           var color = getRandomColor();
           preparedData.colors.push(color);
           
           $.each(dicts.sections[v[0]].subsections, function(sub_key, sub_value){
               if(subvalues[sub_key]){
                    preparedData.labels.push(sub_value.name);
                    preparedData.data.push(subvalues[sub_key]);
                    preparedData.colors.push(color);
               }
           });
        });

        return preparedData;
    },

});

var countryChart = $.extend({}, customChart, {
    selectors: { bar: "#chart_bar--country", doughnut: "#chart_doughnut--country"},
    prepareData: function(rawValues) {
        var sortedValues = Object.keys(rawValues).map((id) => [id, rawValues[id], dicts.countries[id]]);
        sortedValues.sort((i1, i2) => i2[1] - i1[1]);

        var preparedData = {
            labels: [],
            data: [],
            colors: []
        };
        $.each(sortedValues, function(i, v){
           preparedData.labels.push(v[2]);
           preparedData.data.push(v[1]);
           preparedData.colors.push(getRandomColor());
        });

        return preparedData;
    },
});

var nopChart = $.extend({}, customChart, {
    selectors: { bar: "#chart_bar--nop", doughnut: "#chart_doughnut--nop"},
    prepareData: function(rawValues) {
        var sortedValues = Object.keys(rawValues).map((id) => [id, rawValues[id], id]);
        sortedValues.sort((i1, i2) => i2[1] - i1[1]);

        var preparedData = {
            labels: [],
            data: [],
            colors: []
        };
        $.each(sortedValues, function(i, v){
           preparedData.labels.push(v[2]);
           preparedData.data.push(v[1]);
           preparedData.colors.push(getRandomColor());
        });

        return preparedData;
    },
});