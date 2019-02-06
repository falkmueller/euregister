function getRandomColor() {
    return "rgba(" + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ", 0.8)"
}

function prepareData(rawValues) {
    var sortedValues = Object.keys(rawValues).map((id) => [id, rawValues[id]]);
    sortedValues.sort((i1, i2) => i2[1].count - i1[1].count);

    var preparedData = {
        labels: [],
        data: [],
        colors: []
    };
    $.each(sortedValues, function(i, v){
        /*datasets.push({
            label: code,
            data: [size],
            backgroundColor: getColor(1),
            borderWidth: 1
        });*/
       preparedData.labels.push(v[1].name);
       preparedData.data.push(v[1].count);
       preparedData.colors.push(getRandomColor());
    });

    return preparedData;
}

function drawDoughnutChart(values) {
    var data = prepareData(values);
    
    $('#country_chart_bar').hide();
    $('#country_chart_doughnut').show();
    $('#country_chart_doughnut').height(500 + data.data.length * 2);
    var ctx = document.getElementById("country_chart_doughnut");
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
                display: true,
                text: 'Registered companies per country'
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    return myChart;
}

function drawBarChart(values) {
    var data = prepareData(values);
    
    $('#country_chart_doughnut').hide();
    $('#country_chart_bar').show();
    $('#country_chart_bar').height(data.data.length * 12);
    var ctx = document.getElementById("country_chart_bar");
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
                display: true,
                text: 'Registered companies per country'
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

function clearChart(app) {
    if (!app) return;
    if (app.chart) {
        // remove and re-add the canvas element to wipe all lingering event handlers
        var clonedCanvas = app.chart.canvas.cloneNode();
        var nextSibling = app.chart.canvas.nextSibling;
        var parent = app.chart.canvas.parentNode;
        app.chart.canvas.remove();
        app.chart.destroy();
        parent.insertBefore(clonedCanvas, nextSibling);
    }
    app.chart = null;
}
