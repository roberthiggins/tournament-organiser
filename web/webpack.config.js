var ExtractTextPlugin = require("extract-text-webpack-plugin"),
    webpack = require("webpack");

module.exports = {
  entry: {
    // GLOBAL COMPONENTS
    style: './src/static/style.css',
    menu: './src/views/component-menu.js',

    // CONTROLLER ROUTES
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
    userDetails: './src/views/user-details.js',
    userUpdate: './src/views/user-update.js',
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
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract("style-loader", "css-loader")
      },
      {
        test: /\.gif$|\.png$/, //|\.svg$|\.woff$|\.ttf$|\.wav$|\.jpe?g$|\.mp3$/,
        loader: 'file'
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin("style.css", {allChunks: true}),
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
