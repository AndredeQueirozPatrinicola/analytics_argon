const path = require('path');

module.exports = {
  entry: './apps/frontend/index.js',
  output: {
    path: path.resolve(__dirname, 'apps', 'static', 'assets', 'js'),
    filename: 'bundle.js',
  },
};