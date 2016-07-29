module.exports = {
  entry: {
    devindex: './src/views/devindex.js',
    feedback: './src/views/feedback.js',
    login: './src/views/login.js',
    signup: './src/views/signup.js',
    tournamentDraw: './src/views/tournament-draw.js',
    tournamentInfo: './src/views/tournament-info.js',
    tournamentList: './src/views/tournament-list.js'
  },
  output: {
    path: './public',
    filename: '[name].js'
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
