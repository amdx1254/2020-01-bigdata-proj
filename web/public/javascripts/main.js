(function($) {
    // Set new default font family and font color to mimic Bootstrap's default styling
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';

    function number_format(number, decimals, dec_point, thousands_sep) {
        // *     example: number_format(1234.56, 2, ',', ' ');
        // *     return: '1 234,56'
        number = (number + '').replace(',', '').replace(' ', '');
        var n = !isFinite(+number) ? 0 : +number,
            prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
            sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
            dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
            s = '',
            toFixedFix = function(n, prec) {
                var k = Math.pow(10, prec);
                return '' + Math.round(n * k) / k;
            };
        // Fix for IE parseFloat(0.55).toFixed(0) = 0;
        s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
        if (s[0].length > 3) {
            s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
        }
        if ((s[1] || '').length < prec) {
            s[1] = s[1] || '';
            s[1] += new Array(prec - s[1].length + 1).join('0');
        }
        return s.join(dec);
    }

    let createAmountLineChart = function(cflist, cbflist) {
        let arrx = ['0-10000', '10000-20000', '20000-30000', '30000-40000', '40000-50000', '50000-100000', '100000-'];
        let cfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);
        let cbfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);

        for (let cfy of cflist) {
            if (cfy.amount < 10000 && cfy.amount >= 0) {
                cfAreaY[0] += 1;
            } else if (cfy.amount < 20000 && cfy.amount >= 10000) {
                cfAreaY[1] += 1;
            } else if (cfy.amount < 30000 && cfy.amount >= 20000) {
                cfAreaY[2] += 1;
            } else if (cfy.amount < 40000 && cfy.amount >= 30000) {
                cfAreaY[3] += 1;
            } else if (cfy.amount < 50000 && cfy.amount >= 40000) {
                cfAreaY[4] += 1;
            } else if (cfy.amount < 100000 && cfy.amount >= 50000) {
                cfAreaY[5] += 1;
            } else {
                cfAreaY[6] += 1;
            }
        }
        for (let cbfy of cbflist) {
            if (cbfy.amount < 10000 && cbfy.amount >= 0) {
                cbfAreaY[0] += 1;
            } else if (cbfy.amount < 20000 && cbfy.amount >= 10000) {
                cbfAreaY[1] += 1;
            } else if (cbfy.amount < 30000 && cbfy.amount >= 20000) {
                cbfAreaY[2] += 1;
            } else if (cbfy.amount < 40000 && cbfy.amount >= 30000) {
                cbfAreaY[3] += 1;
            } else if (cbfy.amount < 50000 && cbfy.amount >= 40000) {
                cbfAreaY[4] += 1;
            } else if (cbfy.amount < 100000 && cbfy.amount >= 50000) {
                cbfAreaY[5] += 1;
            } else {
                cbfAreaY[6] += 1;
            }
        }
        // areaChart Start
        var ctx = document.getElementById("myAmountChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: arrx,
                datasets: [{
                    label: "Collaborative filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cfAreaY,
                }, {
                    label: "Content Based filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(115, 223, 78, 0.05)",
                    borderColor: "rgba(115, 223, 78, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointBorderColor: "rgba(115, 223, 78, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointHoverBorderColor: "rgba(115, 223, 78, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cbfAreaY,
                }],
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        fontColor: 'black'
                    }
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Amount'
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            maxTicksLimit: 5,
                            padding: 10,
                            // Include a dollar sign in the ticks
                            callback: function(value, index, values) {
                                return number_format(value);
                            }
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [2],
                            zeroLineBorderDash: [2]
                        }
                    }],
                },
                tooltips: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    titleMarginBottom: 10,
                    titleFontColor: '#6e707e',
                    titleFontSize: 14,
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    intersect: false,
                    mode: 'index',
                    caretPadding: 10,
                    callbacks: {
                        label: function(tooltipItem, chart) {
                            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
                        }
                    }
                }
            }
        });
        //  areaChart End
    }

    let createCategoryLineChart = function(arrx, cflist, cbflist) {

        let cfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);
        let cbfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);

        for (let idx in arrx) {
            for (let cfy of cflist) {
                if (cfy.category == arrx[idx]) {
                    cfAreaY[idx] += 1;
                }
            }
            for (let cbfy of cbflist) {
                if (cbfy.category == arrx[idx]) {
                    cbfAreaY[idx] += 1;
                }
            }
        }
        // areaChart Start
        var ctx = document.getElementById("myCategoryChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: arrx,
                datasets: [{
                    label: "Collaborative filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cfAreaY,
                }, {
                    label: "Content Based filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(115, 223, 78, 0.05)",
                    borderColor: "rgba(115, 223, 78, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointBorderColor: "rgba(115, 223, 78, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointHoverBorderColor: "rgba(115, 223, 78, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cbfAreaY,
                }],
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        fontColor: 'black'
                    }
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Category'
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            maxTicksLimit: 5,
                            padding: 10,
                            // Include a dollar sign in the ticks
                            callback: function(value, index, values) {
                                return number_format(value);
                            }
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [2],
                            zeroLineBorderDash: [2]
                        }
                    }],
                },
                tooltips: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    titleMarginBottom: 10,
                    titleFontColor: '#6e707e',
                    titleFontSize: 14,
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    intersect: false,
                    mode: 'index',
                    caretPadding: 10,
                    callbacks: {
                        label: function(tooltipItem, chart) {
                            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
                        }
                    }
                }
            }
        });
        //  areaChart End
    }

    let createScoreLineChart = function(arrx, cflist, cbflist) {

        let cfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);
        let cbfAreaY = Array.apply(null, new Array(arrx.length)).map(Number.prototype.valueOf, 0);

        for (let idx in arrx) {
            for (let cfy of cflist) {
                if (cfy.id == arrx[idx]) {
                    cfAreaY[idx] = (cfy.score * 100).toFixed(2);
                }
            }
            for (let cbfy of cbflist) {
                if (cbfy.id == arrx[idx]) {
                    cbfAreaY[idx] = (cbfy.score * 100).toFixed(2);
                }
            }
        }
        // areaChart Start
        var ctx = document.getElementById("myScoreChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: arrx,
                datasets: [{
                    label: "Collaborative filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cfAreaY,
                }, {
                    label: "Content Based filtering",
                    lineTension: 0.3,
                    backgroundColor: "rgba(115, 223, 78, 0.05)",
                    borderColor: "rgba(115, 223, 78, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointBorderColor: "rgba(115, 223, 78, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(115, 223, 78, 1)",
                    pointHoverBorderColor: "rgba(115, 223, 78, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: cbfAreaY,
                }],
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        fontColor: 'black'
                    }
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'name'
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            maxTicksLimit: 5,
                            padding: 10,
                            // Include a dollar sign in the ticks
                            callback: function(value, index, values) {
                                return number_format(value) + '%';
                            }
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [2],
                            zeroLineBorderDash: [2]
                        }
                    }],
                },
                tooltips: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    titleMarginBottom: 10,
                    titleFontColor: '#6e707e',
                    titleFontSize: 14,
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    intersect: false,
                    mode: 'index',
                    caretPadding: 10,
                    callbacks: {
                        label: function(tooltipItem, chart) {
                            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + '%';
                        }
                    }
                }
            }
        });
        //  areaChart End
    }

    $(document).on('click', '.search-btn', function(e) {
        let user_id = $('#user-input').val();
        $('.cf-item').empty();
        let cflist = [];
        let cbflist = [];
        let arrName = new Set();
        let arrCategory = new Set();
        $.ajax({
            method: "GET",
            url: "http://localhost:3000/api/filtering/cf",
            async: false,
            data: { user_id: user_id },
            success: function(data) {
                for (let i of data.item) {
                    cflist.push(i);
                    arrName.add(i.id);
                    arrCategory.add(i.category);
                    let score = i.score * 100;
                    let at = '                          <div class="col-xl-3 col-md-6 mb-4">\
                    <div class="card border-left-info shadow h-100 py-2">\
                        <div class="card-body">\
                            <div class="row no-gutters align-items-center">\
                                <div class="col mr-2">\
                                    <div class="text-s font-weight-bold text-info text-uppercase mb-1">' + i.name + '</div>\
                                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">' + i.amount + '원</div>\
                                    <div class="row no-gutters align-items-center">\
                                        <div class="col-auto">\
                                            <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' + score.toFixed(2) + '%</div>\
                                        </div>\
                                        <div class="col">\
                                            <div class="progress progress-sm mr-2">\
                                                <div class="progress-bar bg-info" role="progressbar" style="width: ' + score.toFixed(2) + '%" aria-valuenow="' + score.toFixed(2) + '" aria-valuemin="0" aria-valuemax="100"></div>\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                                <div class="col-auto">\
                                    <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </div>';

                    $('.cf-item').append(at);
                }
            }
        });
        $('.cbf-item').empty();
        $.ajax({
            method: "GET",
            url: "http://localhost:3000/api/filtering/cbf",
            async: false,
            data: { user_id: user_id },
            success: function(data) {
                for (let i of data.item) {
                    cbflist.push(i);
                    arrName.add(i.id);
                    arrCategory.add(i.category);
                    let score = i.score * 100;
                    let at = '                          <div class="col-xl-3 col-md-6 mb-4">\
                    <div class="card border-left-info shadow h-100 py-2">\
                        <div class="card-body">\
                            <div class="row no-gutters align-items-center">\
                                <div class="col mr-2">\
                                    <div class="text-s font-weight-bold text-info text-uppercase mb-1">' + i.name + '</div>\
                                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">' + i.amount + '원</div>\
                                    <div class="row no-gutters align-items-center">\
                                        <div class="col-auto">\
                                            <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' + score.toFixed(2) + '%</div>\
                                        </div>\
                                        <div class="col">\
                                            <div class="progress progress-sm mr-2">\
                                                <div class="progress-bar bg-info" role="progressbar" style="width: ' + score.toFixed(2) + '%" aria-valuenow="' + score.toFixed(2) + '" aria-valuemin="0" aria-valuemax="100"></div>\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                                <div class="col-auto">\
                                    <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </div>';

                    $('.cbf-item').append(at);
                }
            }
        });
        let scoreChart = '<div class="chart-area">\
                                <canvas id="myScoreChart"></canvas>\
                            </div>'
        $('#score-chart').empty();
        $('#score-chart').append(scoreChart);
        let categoryChart = '<div class="chart-area">\
                                <canvas id="myCategoryChart"></canvas>\
                            </div>'
        $('#category-chart').empty();
        $('#category-chart').append(categoryChart);
        let amountChart = '<div class="chart-area">\
                                <canvas id="myAmountChart"></canvas>\
                            </div>'
        $('#amount-chart').empty();
        $('#amount-chart').append(amountChart);
        createScoreLineChart(Array.from(arrName), cflist, cbflist);
        createCategoryLineChart(Array.from(arrCategory), cflist, cbflist);
        createAmountLineChart(cflist, cbflist);
    });

})(jQuery);