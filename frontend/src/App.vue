<template>
  <div id="app">
    <header>
      <nav class="navbar navbar-expand-md navbar-light bg-light fix-top">
        <a class="navbar-brand" href="#">
          <img class="img-thumbnil" src="data/icon.jpg" width="40" height="40" alt>
        </a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="#">Vtuber DashBoard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#"></a>
            </li>
            <li class="nav-item active">
              <!-- <a class="nav-link" href="#">
                Contorler
                <span class="sr-only">(current)</span>
              </a>-->
              <a
                class="btn btn-outline-success my-2 my-sm-0"
                data-toggle="collapse"
                href="#filter-panel"
                role="button"
                aria-expanded="false"
                aria-controls="filter-panel"
              >Filter</a>
            </li>
          </ul>
        </div>
      </nav>
    </header>
    <main role="main" class="flex-shrink-0 fill">
      <div class="container-fluid h-100">
        <div class="row fill">
          <!-- the main part for graph pannel -->
          <div class="col-9">
            <vtb-graph
              v-bind:graphData="graphData"
              v-bind:vtbData="vtbData"
              v-on:setCurrentVtb="setCurrentVtb"
              v-on:setGraph="setGraph"
            ></vtb-graph>
          </div>
          <!-- this is the info pannel for vtuber -->
          <div class="col">
            <vtb-info v-bind:vtb="currentVtb" v-bind:thumbnil="thumbnil"></vtb-info>
          </div>
        </div>
      </div>
    </main>

    <footer class="footer mt-auto py-3">
      <div class="container text-center">
        <strong>Powered With &#x2764;</strong>
        <span class="text-mute">by StarGazerMiao & Friends</span>
      </div>
    </footer>
  </div>
</template>

<script>
import VtbGraph from "./components/VtbGraph.vue";
import VtbInfo from "./components/VtbInfo.vue";

import axios from "axios";

export default {
  name: "app",
  components: {
    VtbGraph,
    VtbInfo
  },
  data: function() {
    return {
      graphData: undefined,
      vtbData: undefined,
      currentVtb: {
        name: "Kizuna Ai",
        channel: "A.I. Channel"
      },
      thumbnil: "data/thumbnil/A.I.Channel.jpg"
    };
  },
  methods: {
    setCurrentVtb: function(vtb) {
      this.currentVtb = vtb;
      this.thumbnil =
        "data/thumbnil/" + encodeURI(vtb.channel.replace("/", "_")) + ".jpg";
    },
    setGraph: function(g) {
      let _this = this
      let graphURI = "data/" + g + ".gexf";
      axios({
        method: "get",
        url: graphURI,
        responseType: "xml"
      }).then(function(res) {
        _this.graphData = res.data;
      });
    }
  },
  mounted: function() {
    let _this = this;
    axios({
      method: "get",
      url: "data/No-Clusting.gexf",
      responseType: "xml"
    }).then(function(res) {
      _this.graphData = res.data;
    });
    axios.get("data/vtuber.json").then(function(res) {
      _this.vtbData = JSON.parse(JSON.stringify(res.data));
    });
  }
};
</script>

<style scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

main > .container {
  padding: 60px 15px 0;
}

.footer {
  background-color: #f5f5f5;
}

.footer > .container {
  padding-right: 15px;
  padding-left: 15px;
}

code {
  font-size: 80%;
}

.h-90 {
  height: 90% !important;
}

.fill {
  min-height: 87vh;
}
</style>