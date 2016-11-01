/* global $ React ReactDOM:true */
var borderStyle = {border: "1px solid"};

var GameRow = React.createClass({
    propTypes: {
        game: React.PropTypes.object.isRequired
    },
    render: function(){
        return (
            <tr>
                <td style={borderStyle}>{this.props.game.table_number}</td>
                <td style={borderStyle}>{this.props.game.entrants[0]}</td>
                <td style={borderStyle}>{this.props.game.entrants[1]}</td>
            </tr>
        );
    }
});

var Draw = React.createClass({
    propTypes: {
        draw:    React.PropTypes.array.isRequired,
        mission: React.PropTypes.string.isRequired,
        round:   React.PropTypes.string.isRequired,
        tourn:   React.PropTypes.string.isRequired
    },
    render: function() {
        var games = this.props.draw.map(function(game, idx) {
                return (
                    <GameRow game={game} key={idx} />
                );
            });
        return (
            <div>
                <h2>Draw for Round {this.props.round}, {this.props.tourn}</h2>
                <div>Mission: {this.props.mission}</div>
                <table style={borderStyle}>
                    <thead>
                        <tr>
                            <td style={borderStyle}>Table</td>
                            <td style={borderStyle}>Player 1</td>
                            <td style={borderStyle}>Player 2</td>
                        </tr>
                    </thead>
                    <tbody>
                        {games}
                    </tbody>
                </table>
            </div>
        );
    }
});

var TournamentDrawPagePage = React.createClass({
    getInitialState: function() {
        return ({
            draw: null,
            error: "",
            mission: "",
            round: "",
            tournament: ""
        });
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {

        var msg = this.state.error ? this.state.error : "No draw is available",
            widget = this.state.draw && this.state.draw.length ?
                <Draw draw={this.state.draw}
                      mission={this.state.mission}
                      round={this.state.round}
                      tourn={this.state.tournament} />
            : <div>{msg}</div>;

        return (
            <div>{widget}</div>
        );
    }
});

ReactDOM.render(
    <TournamentDrawPagePage />,
    document.getElementById("content")
);
