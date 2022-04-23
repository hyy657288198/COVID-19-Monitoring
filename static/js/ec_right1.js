const ec_right1 = echarts.init(document.getElementById('r1'), "dark");
var ec_right1_option = {
    title: {
        text: "Top 5 Provinces with Remaining Diagnosis",
        textStyle: {
            color: 'white',
        },
        left: 'left'
    },
    color: ['#3398DB'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    xAxis: {
        type: 'category',
        color: 'white',
        data: []
    },
    yAxis: {
        type: 'value',
        color: 'white',
    },
    series: [{
        data: [],
        type: 'bar',
        barMaxWidth: "50%"
    }]
};
ec_right1.setOption(ec_right1_option)
