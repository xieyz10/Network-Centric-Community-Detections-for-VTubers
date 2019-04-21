<template>
  <div id="VtbGraph" class="fill">
    <div id="graph-filter">
      <div class="collapse" id="filter-panel">
        <div class="card card-body">
          <div class="row">
            <label for="clusting" class="col-md-1 col-form-label">Clusting</label>
            <select id="clusting" v-model="clusting" class="form-control col-md-2">
              <option>Max-Clique</option>
              <option>Quasi-Clique</option>
              <option>K-Means</option>
            </select>
            <div class="input-group mb-3 col-sm-8">
              <div class="input-group-prepend">
                <span class="input-group-text" id="filter-weight">hide weight</span>
              </div>
              <input
                type="text"
                class="form-control col-sm-1"
                placeholder="weight size"
                aria-label="weight size"
                aria-describedby="filter-weight"
                v-model="smallEdgeGate"
              >
              <div class="input-group-prepend" style="margin-left:10px">
                <span class="input-group-text" id="filter-name">channel name</span>
              </div>
              <input
                type="text"
                class="form-control col-sm-2"
                placeholder="channel name"
                aria-label="channel name"
                aria-describedby="filter-name"
                v-model="selectedChannel"
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="chart" class="vtb-graph"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import axios from "axios";
import "echarts/extension/dataTool";

export default {
  name: "VtbGraph",
  props: {
    graphData: undefined,
    vtbData: undefined
  },
  data: function() {
    return {
      chart: undefined,
      graph: undefined,
      smallEdgeGate: 3,
      selectedChannel: "",
      clusting: ""
    };
  },
  methods: {
    drawVtbGraph: function(data) {
      console.log("drawing");
      let _this = this;
      var vtbchart = echarts.init(document.getElementById("chart"));
      var showEdges = [];

      vtbchart.hideLoading();

      var graph = echarts.dataTool.gexf.parse(data);
      // var categories = [];
      // for (var i = 0; i < 9; i++) {
      //   categories[i] = {
      //     name: '类目' + i
      //   };
      // }

      graph.nodes.forEach(function(node) {
        node.value = node.symbolSize;
        node.symbolSize /= 2;
        node.label = {
          normal: {
            color: "#000",
            show: node.symbolSize > 20
          }
        };
        node.category = node.attributes.mod;
        // node.symbol = 'image://data/thumbnil/' + node.name + '.jpg';
        // set the node texture
        node.itemStyle.normal.borderColor = "#fff";
        node.itemStyle.normal.borderWidth = 1;
        node.itemStyle.normal.shadowBlur = 10;
        node.itemStyle.normal.shadowColor = "rgba(0, 0, 0, 0.3)";
      });

      graph.links.forEach(function(edge) {
        edge.value = edge.weight;
        var myColor = 1 / edge.weight;
        if (parseInt(edge.weight) > parseInt(_this.smallEdgeGate)) {
          // edge.lineStyle = {
          //   width: 0
          // };
          // } else {
          edge.label = {
            show: true,
            formatter: "{c}"
          };
          // find source node
          //let source = undefined;
          let sourceColor = "rgba(0, 0, 0, 1)";
          for(let i = 0; i < graph.nodes.length; i++){
            if(parseInt(edge.source) == parseInt(graph.nodes[i].id)){
              sourceColor = graph.nodes[i].itemStyle.normal.color;
            }
          }
          // drop a in rgaba
          let sourceColorArray = sourceColor.split(",");
          sourceColorArray.pop();
          let sourceColorBase = sourceColorArray.join(",");

          if (edge.weight > 50) {
            edge.lineStyle = {
              color: sourceColor,
              curveness: 0.3
            };
          } else if (edge.weight > 40) {
            edge.lineStyle = {
              color: sourceColorBase + ",0.8)",
              curveness: 0.3
            };
          } else if (edge.weight > 30) {
            edge.lineStyle = {
              color: sourceColorBase + ",0.6)",
              curveness: 0.3
            };
          } else if (edge.weight > 20) {
            edge.lineStyle = {
              color: sourceColorBase + "0.4)",
              curveness: 0.3
            };
          } else if (edge.weight > 10) {
            edge.lineStyle = {
              color: sourceColorBase + ",0.3)",
              curveness: 0.3
            };
          } else {
            edge.lineStyle = {
              color: sourceColorBase + ",0.3)",
              curveness: 0.3
            };
          }
          showEdges.push(edge);
        }
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
            links: showEdges,
            roam: true,
            focusNodeAdjacency: true,
            // label: {
            //   position: "right",
            //   formatter: "{b}"
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
      // document.oncontextmenu = function() {
      //   return false;
      // };
      _this.chart = vtbchart;
      _this.graph = graph;
    }
  },
  // updated: () => {
  //   this.drawVtbGraph(this.graphData);
  // },
  watch: {
    graphData: function() {
      this.drawVtbGraph(this.graphData);
    },
    smallEdgeGate: function() {
      // console.log(this.smallEdgeGate);
      this.drawVtbGraph(this.graphData);
    },
    selectedChannel: function() {
      var _this = this;
      //let nodeNum = 0;
      //console.log(this.graph.nodes)
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.selectedChannel == this.graph.nodes[i].name) {
          this.chart.dispatchAction({
            type: "focusNodeAdjacency",
            dataIndex: i
          });
        }
      }
      //console.log(this.graph.nodes);
    },
    clusting: function() {
      // let _this = this;
      // if (_this.clustingAlogorithm == "Quasi-Clique") {
      // } else if (_this.clustingAlogorithm == "K-Means") {
      // } else if (_this.clustingAlogorithm == "Max-Clique") {
      //   _this.chart.showLoading();
      //   axios.get("data/vtuber-clique.json").then(function(res) {
      //     _this.vtbData = JSON.parse(JSON.stringify(res.data));
      //   });
      // }
      this.$emit("setGraph", this.clusting);
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

<<<<<<< HEAD
  .fill {
    width: 100%;
    height: 80%;
  }
=======
.fill {
  width: 100%;
  height: 50%;
}

.graph-filter {
  margin-top: 5px;
}
button {
  margin: 10px;
}
>>>>>>> 0e696e0016fb8ce85dd79e099acc7b70f001ce46
</style>