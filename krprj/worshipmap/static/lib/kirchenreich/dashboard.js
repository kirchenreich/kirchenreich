if (kr === undefined) {
    var kr = {};
}

kr.colors = {
    yellow: '#ffc40d',
    blue: '#049cdb',
    red: '#9d261d',
    green: '#46a546'
};

kr.plot = {};
kr.plot.pie = function(target, data) {
    $.plot($(target), data, {
        series: {
            pie: {
                show: true,
                label: {
                    show: true,
                    radius: 3/4,
                    formatter: function(label, series){
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
                    },
                    background: {
                        opacity: 0.5,
                        color: '#000'
                    }
                }
            }
        },
        legend: {
            show: false
        }
    });
};

kr.plot.onCheckHover = function(event, check){
    var _data;
    if (check === undefined) {
        _data = $(this).data();
    } else {
        _data = $(check).data();
    }

    var data = [{
        label: 'Reached',
        data: _data.reached,
        color: kr.colors.green
    }, {
        label: 'Pending',
        data: _data.pending,
        color: kr.colors.red
    }];
    kr.plot.pie('#check_plot', data);
};

$(document).ready(function() {
    $("tr.kr_check").hover(kr.plot.onCheckHover);
    kr.plot.onCheckHover({}, $("tr.kr_check").first());
});

