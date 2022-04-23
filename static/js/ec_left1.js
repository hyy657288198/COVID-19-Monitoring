const ec_left1 = echarts.init(document.getElementById('l1'), "dark");
const ec_left1_Option = {
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'line',
			lineStyle: {
				color: '#7171C6'
			}
		},
	},
	legend: {
		data: ['New Diagnosis', 'New Heal'],
		left: "right",
		orient: "vertical"
	},
	title: {
		text: "Trend of New Diagnosis and Heal",
		textStyle: {
			color: 'white',
		},
		left: 'left'
	},
	grid: {
		left: '4%',
		right: '6%',
		bottom: '4%',
		top: 50,
		containLabel: true
	},
	xAxis: [{
		type: 'category',
		data: []
	}],
	yAxis: [{
		type: 'value',

		axisLine: {
			show: true
		},
		axisLabel: {
			show: true,
			color: 'white',
			fontSize: 12,
			formatter: function (value) {
				if (value >= 1000) {
					value = value / 1000 + 'k';
				}
				return value;
			}
		},
		splitLine: {
			show: true,
			lineStyle: {
				width: 1,
			}
		}
	}],
	series: [{
		name: "New Diagnosis",
		type: 'line',
		smooth: true,
		data: []
	}, {
		name: "New Heal",
		type: 'line',
		smooth: true,
		data: []
	}]
};

ec_left1.setOption(ec_left1_Option);
