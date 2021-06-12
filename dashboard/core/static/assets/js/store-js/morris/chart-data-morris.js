// First Chart Example - Area Line Chart

Morris.Donut({
  element: 'morris-chart-donut',
//  data: [
//    {label: "Active", value: 12},
//    {label: "Warning", value: 25},
//    {label: "Error", value: 27}
//  ],
  data: javascript_array,
  colors: ['#22aa22' ,'#FFD200', '#ff0000'],
  formatter: function (y) { return y ;}
});

Morris.Line({
  // ID of the element in which to draw the chart.
  element: 'morris-chart-line',
  // Chart data records -- each entry in this array corresponds to a point on
  // the chart.
  data: [
	{ d: '2012-10-01', visits: 82 , a:20},
	{ d: '2012-10-02', visits: 83 , a:47},
	{ d: '2012-10-03', visits: 20 , a:83},
	{ d: '2012-10-04', visits: 39 , a:46},
	{ d: '2012-10-05', visits: 92 , a:32},
	{ d: '2012-10-06', visits: 59 , a:13},
	{ d: '2012-10-07', visits: 90 , a:94},
	{ d: '2012-10-08', visits: 80 , a:25},
	{ d: '2012-10-09', visits: 92 , a:74},
	{ d: '2012-10-10', visits: 20 , a:13},
	{ d: '2012-10-11', visits: 82 , a:47},
	{ d: '2012-10-12', visits: 89 , a:53},
	{ d: '2012-10-13', visits: 19 , a:11},
	{ d: '2012-10-14', visits: 49 , a:76},
	{ d: '2012-10-15', visits: 70 , a:12},
	{ d: '2012-10-16', visits: 63 , a:57},
	{ d: '2012-10-17', visits: 92 , a:18},
	{ d: '2012-10-18', visits: 24 , a:18},
	{ d: '2012-10-19', visits: 29 , a:27},
	{ d: '2012-10-20', visits: 29 , a:76},
	{ d: '2012-10-21', visits: 39 , a:65},
	{ d: '2012-10-22', visits: 90 , a:52},
	{ d: '2012-10-23', visits: 12 , a:74},
	{ d: '2012-10-24', visits: 93 , a:45},
	{ d: '2012-10-25', visits: 83 , a:56},
	{ d: '2012-10-26', visits: 48 , a:76},
	{ d: '2012-10-27', visits: 23 , a:34},
	{ d: '2012-10-28', visits: 90 , a:24},
	{ d: '2012-10-29', visits: 20 , a:63},
	{ d: '2012-10-30', visits: 29 , a:42},
	{ d: '2012-10-31', visits: 92 , a:85}
  ],
//  data: javascript_array,
  // The name of the data record attribute that contains x-visitss.
  xkey: 'd',
  // A list of names of data record attributes that contain y-visitss.
  ykeys: ['visits','a'],
  labels: ['Warning','Error'],
  lineColors: ['#FFD200', '#22aa22'], //line color orange green
  lineWidth: ['5px'],
  // Disables line smoothing
  smooth: false,
});

Morris.Bar ({
  element: 'morris-chart-bar',
  data: [
	{device: 'iPhone', geekbench: 136},
	{device: 'iPhone 3G', geekbench: 137},
	{device: 'iPhone 3GS', geekbench: 275},
	{device: 'iPhone 4', geekbench: 380},
	{device: 'iPhone 4S', geekbench: 655},
	{device: 'iPhone 5', geekbench: 1571}
  ],
  xkey: 'device',
  ykeys: ['geekbench'],
  labels: ['Geekbench'],
  barRatio: 0.4,
  xLabelAngle: 35,
  hideHover: 'auto'
});
