import "jquery";
import { dataTool, init } from 'echarts';
import "echarts/src/chart/graph";
import "echarts/extension/dataTool";

window.onload = function () {

  var vtbchart = init(document.getElementById("chart"));

  $.get('data/mock.gexf',
    function (xml) {
      vtbchart.hideLoading()

      var graph = dataTool.gexf.parse(xml);
      // var categories = [];
      // for (var i = 0; i < 9; i++) {
      //   categories[i] = {
      //     name: '类目' + i
      //   };
      // }
      graph.nodes.forEach(function (node) {
        console.log(node)
        node.itemStyle = null;
        node.value = node.symbolSize;
        node.symbolSize *= 2;
        node.label = {
          normal: {
            show: node.symbolSize > 30
          }
        };
        node.category = node.attributes.mod;
        node.symbol = 'image://data/thumbnil/' + node.name + '.jpg';
      });
      option = {
        title: {
          text: 'Vtuber Relation',
          subtext: 'Default layout',
          top: 'bottom',
          left: 'right'
        },
        tooltip: {},
        // legend: [{
        //   // selectedMode: 'single',
        //   data: categories.map(function (a) {
        //     return a.name;
        //   })
        // }],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            name: 'Vtuber Relation',
            type: 'graph',
            layout: 'none',
            data: graph.nodes,
            links: graph.links,
            roam: true,
            focusNodeAdjacency: true,
            itemStyle: {
              normal: {
                borderColor: '#fff',
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
              }
            },
            label: {
              position: 'right',
              formatter: '{b}'
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            },
            emphasis: {
              lineStyle: {
                width: 10
              }
            }
          }
        ]
      };
      vtbchart.setOption(option);
    }, 'xml');
};