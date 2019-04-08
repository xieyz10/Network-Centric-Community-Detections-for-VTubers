const path = require('path');

module.exports = {
  entry: './src/show.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  // resolve: {
  //     alias: {
  //       echarts$: "echarts/src/echarts.js",
  //       echarts: "echarts",
  //       zrender$: "zrender/src/zrender.js",
  //       zrender: "zrender/src"
  //   }
  // }
};