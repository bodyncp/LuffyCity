//
// $.ajax({
//     url: '/getdata/',
//     type: "get",
//     success: function (data) {
//         var getdate = data.data;
//         Highcharts.chart('contain', {
//             title: {
//                 style: {
//                     "fontFamily": "\"微软雅黑\", Arial, Helvetica, sans-serif",
//                     "color": (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
//                     "fontSize": "10px",
//                     "fontWeight": "normal",
//                     "fontStyle": "normal"
//                 },
//                 text: '总代码量排行'
//             },
//             exporting: {
//                 "enabled": false,
//                 "fallbackToExportServer": false
//             },
//             tooltip: {
//                 pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
//             },
//             plotOptions: {
//                 pie: {
//                     allowPointSelect: true,
//                     cursor: 'pointer',
//                     depth: 20,
//                     dataLabels: {
//                         enabled: true,
//                         format: '{point.name}'
//                     }
//                 }
//             },
//             style: {
//                 color: '#ff0000',
//                 fontSize: "2px",
//                 fontFamily: "Courier new"
//             },
//             series: [{
//                 type: 'pie',
//                 name: '总代码量排行',
//                 data:
//                 getdate
//             }]
//         })
//     }
// });