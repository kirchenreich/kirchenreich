var kr = {};
kr.color = {
    yellow: '#ffc40d',
    blue: '#049cdb',
    red: '#9d261d',
    green: '#46a546'
};
kr.color.set = [kr.color.yellow, kr.color.blue];

kr.plot = {};
kr.plot.pie = function(target, radius, position, data, legend) {
    var r = Raphael(target, $('#'+target).width(), radius*2);

    var x, legendpos;
    if (position === 'left'){
        x = radius*2;
        legendpos = 'west';
    } else {
        x = radius;
        legendpos = 'east';
    }
    pie = r.piechart(x, radius, radius, data, {
        colors: kr.color.set,
        legend: legend,
        legendpos: legendpos
    });
};

kr.plot.pie_small = function(target, radius, data) {
    var pie = Raphael(target, radius*2, radius*2);
    pie.piechart(radius, radius, radius, data, {
        strokewidth: 0,
        minPercent: 0,
        colors: [kr.color.green, kr.color.red]
    });
};

