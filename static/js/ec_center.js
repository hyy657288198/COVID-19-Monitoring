const ec_center = echarts.init(document.getElementById('c2'), "dark");

var ec_center_option = {
    title: {
        text: 'National Current Diagnosis',
        subtext: '',
        x: 'left'
    },
    tooltip: {
        trigger: 'item'
    },
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
            fontSize: 8,
        },
        splitList: [{ start: 0,end: 0 },
            { start: 1,end: 9 },
            {start: 10, end: 99 },
			{ start: 100, end: 999 },
            {  start: 1000, end: 9999 },
            { start: 10000 }],
        color: ['#8A3310', '#C64918', '#E55B25', '#F2AD92', '#F9DCD1', '#FFF0F5']
    },
    series: [{
        name: 'Current Diagnosis',
        type: 'map',
        mapType: 'china',
        roam: false,
        itemStyle: {
            normal: {
                borderWidth: .5,
                borderColor: '#62d3ff',
                areaColor: "#b7ffe6",
            },
            emphasis: {
                borderWidth: .5,
                borderColor: '#fff',
                areaColor: "#fff",
            }
        },
        label: {
            normal: {
                show: true,
                fontSize: 8,
            },
            emphasis: {
                show: true,
                fontSize: 8,
            }
        },
        data:[]
    }]
};
ec_center.setOption(ec_center_option)
