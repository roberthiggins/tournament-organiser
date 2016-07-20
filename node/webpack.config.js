module.exports = {
  entry: './src/devindex.js',
  output: {
    path: './public',
    filename: 'devindex.js'
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
           presets: ['es2016', 'react']
        }
      }
    ]
  },
  resolve: {
    extensions: ['', '.js', '.json']
  }
};
