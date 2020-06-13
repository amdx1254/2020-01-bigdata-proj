(function($) {

    $(document).on('click', '.search-btn', function(e) {
        var user_id = $('#user-input').text();
        $('.cf-item').empty();
        $.ajax({
            method: "GET",
            url: "http://localhost:3000/api/filtering/cf",
            data: { user_id: user_id },
            success: function(data) {
                console.log(data)
                for (var i of data.item) {
                    var at = '                          <div class="col-xl-3 col-md-6 mb-4">\
                    <div class="card border-left-info shadow h-100 py-2">\
                        <div class="card-body">\
                            <div class="row no-gutters align-items-center">\
                                <div class="col mr-2">\
                                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">' + i.name + '</div>\
                                    <div class="row no-gutters align-items-center">\
                                        <div class="col-auto">\
                                            <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' + i.satisfaction + '%</div>\
                                        </div>\
                                        <div class="col">\
                                            <div class="progress progress-sm mr-2">\
                                                <div class="progress-bar bg-info" role="progressbar" style="width: ' + i.satisfaction + '%" aria-valuenow="' + i.satisfaction + '" aria-valuemin="0" aria-valuemax="100"></div>\
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
            data: { user_id: user_id },
            success: function(data) {
                console.log(data)
                for (var i of data.item) {
                    var at = '                          <div class="col-xl-3 col-md-6 mb-4">\
                    <div class="card border-left-info shadow h-100 py-2">\
                        <div class="card-body">\
                            <div class="row no-gutters align-items-center">\
                                <div class="col mr-2">\
                                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">' + i.name + '</div>\
                                    <div class="row no-gutters align-items-center">\
                                        <div class="col-auto">\
                                            <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">' + i.satisfaction + '%</div>\
                                        </div>\
                                        <div class="col">\
                                            <div class="progress progress-sm mr-2">\
                                                <div class="progress-bar bg-info" role="progressbar" style="width: ' + i.satisfaction + '%" aria-valuenow="' + i.satisfaction + '" aria-valuemin="0" aria-valuemax="100"></div>\
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
    });

})(jQuery);