module.exports = {
  devServer: {
      proxy: {
          '/api': {
              target: 'http://127.0.0.1:5000',  // Point to the Flask server
              ws: true,  // Proxy websockets if needed
              changeOrigin: true,  // Needed for virtual hosted sites
              pathRewrite: { '^/api': '' },  // Rewrite the API path
          },
      }
  }
};
