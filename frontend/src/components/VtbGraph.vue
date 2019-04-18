<template>
  <div id="chart" class="vtb-graph"></div>
</template>

<script>
import * as echarts from "echarts";
require('echarts/dist/extension/dataTool.js')

export default {
  name: "VtbGraph",
  props: {
    graphData: undefined,
    vtbData: undefined
  },
  data: function() {
    return {
      chart: undefined
    };
  },
  methods: {
    drawVtbGraph: function(data) {
      let _this = this;
      var vtbchart = echarts.init(document.getElementById("chart"));

      vtbchart.hideLoading();

      var graph = echarts.dataTool.gexf.parse(data);
      // var categories = [];
      // for (var i = 0; i < 9; i++) {
      //   categories[i] = {
      //     name: '类目' + i
      //   };
      // }
      graph.nodes.forEach(function(node) {
        node.itemStyle = null;
        node.value = node.symbolSize;
        node.symbolSize /= 2;
        node.label = {
          normal: {
            show: node.symbolSize > 10
          }
        };
        node.category = node.attributes.mod;
        // node.symbol = 'image://data/thumbnil/' + node.name + '.jpg';
      });
      var opt = {
        title: {
          text: "Vtuber Relation",
          subtext: "Default layout",
          top: "bottom",
          left: "right"
        },
        tooltip: {},
        // legend: [{
        //   // selectedMode: 'single',
        //   data: categories.map(function (a) {
        //     return a.name;
        //   })
        // }],
        animationDuration: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            name: "Vtuber Relation",
            type: "graph",
            layout: "none",
            data: graph.nodes,
            links: graph.links,
            roam: true,
            focusNodeAdjacency: true,
            itemStyle: {
              normal: {
                borderColor: "#fff",
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: "rgba(0, 0, 0, 0.3)"
              }
            },
            label: {
              position: "right",
              formatter: "{b}"
            },
            lineStyle: {
              color: "source",
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
      vtbchart.setOption(opt);

      // set click listener for vtuber node in graph and pass data back to
      // parent component
      vtbchart.on("click", function(param) {
        // console.log(param.name)
        for (let i = 0; i < _this.vtbData.length; i++) {
          if (param.name == _this.vtbData[i].channel) {
            console.log(_this.vtbData[i].channel);
            _this.$emit("setCurrentVtb", _this.vtbData[i]);
            break;
          }
        }
      });
      this.chart = vtbchart;
    }
  },
  // updated: () => {
  //   this.drawVtbGraph(this.graphData);
  // },
  watch: {
    graphData: function(newData, oldData){
      this.drawVtbGraph(newData);
    }
  }
};
</script>


<style scoped>
.vtb-graph {
  background-color: rgb(235, 232, 232);
  width: 100%;
  height: 100%;
}
</style>
