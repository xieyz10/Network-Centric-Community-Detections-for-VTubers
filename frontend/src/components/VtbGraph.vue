<template>
  <div id="VtbGraph" class="fill">
      <div><input type="text"  v-model="smallEdgeGate" placeholder="edit me"></div>
      <div id="chart" class="vtb-graph"></div>
  </div>
</template>

<script>
  import * as echarts from "echarts";
  import 'echarts/extension/dataTool'

  export default {
    name: "VtbGraph",
    props: {
      graphData: undefined,
      vtbData: undefined
    },
    data: function () {
      return {
        chart: undefined,
        smallEdgeGate: 3
      };
    },
    methods: {
      drawVtbGraph: function (data) {
        console.log("drawing")
        let _this = this;
        var vtbchart = echarts.init(document.getElementById("chart"));
        var myEdges = [];

        vtbchart.hideLoading();

        var graph = echarts.dataTool.gexf.parse(data);
        // var categories = [];
        // for (var i = 0; i < 9; i++) {
        //   categories[i] = {
        //     name: '类目' + i
        //   };
        // }
        var count = 0;
        graph.links.forEach(function (edge) {
          edge.source = edge.source;
          edge.target = edge.target;
          edge.weight = edge.weight;
          edge.value = edge.weight;
          var myColor = 1/edge.weight;
          if(edge.weight < _this.smallEdgeGate){
            edge.lineStyle = {
                width: 0
            }
          }
          else{
            if(edge.weight > 50){
                edge.lineStyle = {
                  color: "rgba(255,0,0,1)",
                  curveness: 0.3
              }
            }
            else if(edge.weight > 40){
                edge.lineStyle = {
                  color: "rgba(255,0,0,0.8)",
                  curveness: 0.3
              }
            }
            else if(edge.weight > 30){
                edge.lineStyle = {
                  color: "rgba(255,0,0,0.6)",
                  curveness: 0.3
              }
            }
            else if(edge.weight > 20){
                edge.lineStyle = {
                  color: "rgba(255,0,0,0.4)",
                  curveness: 0.3
              }
            }
            else if(edge.weight > 10){
                edge.lineStyle = {
                  color: "rgba(255,0,0,0.2)",
                  curveness: 0.3
              }
            }
            else {
                edge.lineStyle = {
                  color: "rgba(255,0,0,0.1)",
                  curveness: 0.3
              }
            }
          }
          
        });
        graph.nodes.forEach(function (node) {
          node.itemStyle = null;
          node.value = node.symbolSize;
          node.symbolSize /= 2;
          node.label = {
            normal: {
              show: node.symbolSize > 50
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
              // label: {
              //   position: "right",
              //   formatter: "{b}"
              // },
              // lineStyle: {
              //   color: "source",
              //   curveness: 0.3
              // },
              emphasis: {
                lineStyle: {
                  width: 10
                }
              }
            }
          ]
        };
        vtbchart.setOption(opt);
        console.log(vtbchart)
        // set click listener for vtuber node in graph and pass data back to
        // parent component
        vtbchart.on("click", function (param) {
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
      graphData: function (newData, oldData) {
        this.drawVtbGraph(newData);
      },
      smallEdgeGate: function(){
        console.log(this.smallEdgeGate);
        this.drawVtbGraph(this.graphData);
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

  .fill {
    width: 100%;
    height: 100%;
  }
</style>