var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var NextGameInfo = React.createClass({
    propTypes: {
        game: React.PropTypes.object.isRequired
    },
    render: function() {
        return (
            <div>
                <ul>
                    <li>Round: {this.props.game.round}</li>
                    <li>Table: {this.props.game.table}</li>
                    <li>Opponent: {this.props.game.opponent}</li>
                    <li>Mission: {this.props.game.mission}</li>
                </ul>
            </div>
        );
    }
});

var EntryNextGamePage = React.createClass({
    getInitialState: function () {
        return({
            message: "Retrieving info for your next game...",
            widget: null
        });
    },
    componentDidMount: function() {
        this.contentRequest = $.get(
            window.location + "/content",
            function(result) {
                var widget = result.nextgame ?
                    <NextGameInfo game={result.nextgame} /> : null;

                this.setState({
                    message: result.error ? result.error : result.message,
                    widget: result.error ? null : widget
                });
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.contentRequest.abort();
    },
    render: function() {
        return (
            <div>
                <div>{this.state.message}</div>
                {this.state.widget}
            </div>
        );
    }
});

ReactDOM.render(
    <EntryNextGamePage />,
    document.getElementById("content")
);

