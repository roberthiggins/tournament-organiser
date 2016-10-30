var webpack = require("webpack");

module.exports = {
  entry: {
    devindex: './src/views/devindex.js',
    entry: './src/views/entry.js',
    entryNextGame: './src/views/entry-next-game.js',
    entryScore: './src/views/entry-score.js',
    feedback: './src/views/feedback.js',
    index: './src/views/index.js',
    login: './src/views/login.js',
    signup: './src/views/signup.js',
    // brackets are some batshit webpack workaround. An entrypoint can't be used
    // as a dependency unless in a list.
    tournamentCategories: ['./src/views/tournament-categories.js'],
    tournamentCreate: './src/views/tournament-create.js',
    tournamentDraw: './src/views/tournament-draw.js',
    tournamentInfo: './src/views/tournament-info.js',
    tournamentList: './src/views/tournament-list.js',
    tournamentMissions: './src/views/tournament-missions.js',
    tournamentRankings: './src/views/tournament-rankings.js',
    tournamentRounds: './src/views/tournament-rounds.js',
    userDetails: './src/views/user-details.js'
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
  plugins: [
    new webpack.ProvidePlugin({
        $: "jquery",
        React: "react",
        ReactDOM: "react-dom"
    })
  ],
  resolve: {
    extensions: ['', '.js', '.json']
  }
};
