function getRandomColor() {
    return "rgba(" + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ","  + Math.floor(Math.random() * 255) + ", 0.8)"
}

function prepareData(rawValues) {
    var sortedValues = Object.keys(rawValues).map((id) => [id, rawValues[id]]);
    sortedValues.sort(function(i1,i2){return i2[1] - i1[1]});

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
       preparedData.labels.push(v[0]);
       preparedData.data.push(v[1]);
       preparedData.colors.push(getRandomColor());
    });

    return preparedData;
}

function drawDoughnutChart(values) {
    var data = prepareData(values);
    
    var ctx = document.getElementById("country_chart");
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data.data,
                backgroundColor: data.colors,
                label: 'Countries'
            }],
            labels: data.labels
        },
        options: {
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Countries'
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
    
    var ctx = document.getElementById("country_chart");
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
                xAxes: [{position: "top"}],
                yAxes: [{position: "left"}]
            }   
        }
    });
    
    return myChart;
}
