$(document).ready(function(){
    var ctx_chart_summary_bar_log = document.getElementById("chart_summary_bar_log").getContext('2d');
    var chart_summary_bar_log = new Chart(ctx_chart_summary_bar_log, {
        type: 'bar',
        data: {
            labels: ["Accounts", "Deposits", "Credits", "Incomes", "Expenses", "Cars"],
            datasets: [{
                label: 'Sum of values in logarithmic scale',
                data: [
                    document.getElementById("chart_wallet_accounts_sum").value,
                    document.getElementById("chart_wallet_deposits_sum").value,
                    document.getElementById("chart_wallet_credits_sum").value,
                    document.getElementById("chart_wallet_incomes_sum").value,
                    document.getElementById("chart_wallet_expenses_sum").value,
                    document.getElementById("chart_wallet_cars_sum").value,
                ],
                backgroundColor: [
                    '#bbdefb',
                    '#c8e6c9',
                    '#ffcdd2',
                    '#f0f4c3',
                    '#d7ccc8',
                    '#f5f5f5'
                ],
                borderColor: [
                    '#0d47a1',
                    '#1b5e20',
                    '#b71c1c',
                    '#827717',
                    '#3e2723',
                    '#212121',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            title: {
                display: true,
                text: 'Monthly summary (logarithmic chart)',
                fontSize: 20
            },
            scales: {
                yAxes: [{
                    type: 'logarithmic',
                    ticks: {
                        beginAtZero:true,
                        callback: function(value, index, values) {
                            return value + ' zł';
                        },
                        fontSize: 8
                    }
                }]
            },
            tooltips: {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItems, data) {
                        return tooltipItems.yLabel + ' zł';
                    }
                }
            },
            legend: {
                position: 'top',
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
    console.log("wallet chart_summary_bar_log (1)");

    var ctx_chart_summary_doughnut_linear = document.getElementById("chart_summary_doughnut_linear").getContext('2d');
    ctx_chart_summary_doughnut_linear.height = 200;
    var chart_summary_doughnut_linear = new Chart(ctx_chart_summary_doughnut_linear, {
        type: 'doughnut',
        data: {
            labels: ["Accounts", "Deposits", "Credits", "Incomes", "Expenses", "Cars"],
            datasets: [{
                data: [
                    document.getElementById("chart_wallet_accounts_sum").value,
                    document.getElementById("chart_wallet_deposits_sum").value,
                    document.getElementById("chart_wallet_credits_sum").value,
                    document.getElementById("chart_wallet_incomes_sum").value,
                    document.getElementById("chart_wallet_expenses_sum").value,
                    document.getElementById("chart_wallet_cars_sum").value,
                ],
                backgroundColor: [
                    '#bbdefb',
                    '#c8e6c9',
                    '#ffcdd2',
                    '#f0f4c3',
                    '#d7ccc8',
                    '#f5f5f5'
                ],
                borderColor: [
                    '#0d47a1',
                    '#1b5e20',
                    '#b71c1c',
                    '#827717',
                    '#3e2723',
                    '#212121',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Monthly summary (linear chart)',
                fontSize: 20
            },
            tooltips: {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItem, data) {
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var currentValue = dataset.data[tooltipItem.index];
                        var label = data.labels[tooltipItem.index];
                        return label + ': ' + currentValue + ' zł';
                    }
                }
            },
            legend: {
                position: 'left',
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
    console.log("wallet chart_summary_doughnut_linear (2)");

    var chart_expenses_doughnut_linear = document.getElementById("chart_expenses_doughnut_linear").getContext('2d');
    chart_expenses_doughnut_linear.height = 200;

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function shadeColor(color, percent) {
        var R = parseInt(color.substring(1,3),16);
        var G = parseInt(color.substring(3,5),16);
        var B = parseInt(color.substring(5,7),16);

        R = parseInt(R * (100 + percent) / 100);
        G = parseInt(G * (100 + percent) / 100);
        B = parseInt(B * (100 + percent) / 100);

        R = (R<255)?R:255;
        G = (G<255)?G:255;
        B = (B<255)?B:255;

        var RR = ((R.toString(16).length==1)?"0"+R.toString(16):R.toString(16));
        var GG = ((G.toString(16).length==1)?"0"+G.toString(16):G.toString(16));
        var BB = ((B.toString(16).length==1)?"0"+B.toString(16):B.toString(16));

        return "#"+RR+GG+BB;
    }

    var wallet_expenses_elements_number = document.getElementById("chart_wallet_expenses_elements_number").value;
    var wallet_expenses_elements_json = jQuery.parseJSON( document.getElementById("chart_wallet_expenses_elements_json").value )
    chart_expenses_doughnut_linear_labels = []
    chart_expenses_doughnut_linear_values = []
    chart_expenses_doughnut_linear_backgroundColor = []
    chart_expenses_doughnut_linear_borderColor = []
    $.each( wallet_expenses_elements_json, function( index, obj ) {
      chart_expenses_doughnut_linear_labels[index] = obj.key;
      chart_expenses_doughnut_linear_values[index] = obj.value;
      chart_expenses_doughnut_linear_backgroundColor[index] = getRandomColor();
      chart_expenses_doughnut_linear_borderColor[index] = shadeColor(chart_expenses_doughnut_linear_backgroundColor[index], -40);
    });

    var chart_expenses_doughnut_linear = new Chart(chart_expenses_doughnut_linear, {
        type: 'doughnut',
        data: {
            labels: chart_expenses_doughnut_linear_labels,
            datasets: [{
                data: chart_expenses_doughnut_linear_values,
                backgroundColor: chart_expenses_doughnut_linear_backgroundColor,
                borderColor: chart_expenses_doughnut_linear_borderColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Expenses summary (' + wallet_expenses_elements_number + ' elements)',
                fontSize: 20
            },
            tooltips: {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItem, data) {
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var currentValue = dataset.data[tooltipItem.index];
                        var label = data.labels[tooltipItem.index];
                        return label + ': ' + currentValue + ' zł';
                    }
                }
            },
            legend: {
                position: 'left',
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
    console.log("wallet chart_expenses_doughnut_linear (3)");
 });