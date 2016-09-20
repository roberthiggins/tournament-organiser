var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var borderStyle = {border: "1px solid"};

var EntryRow = React.createClass({
    propTypes: {
        entry: React.PropTypes.object.isRequired
    },
    render: function(){
        var scores = this.props.entry.scores.map(function(score, idx) {
                return (
                    <td style={borderStyle} key={idx}>{score.score}</td>
                );
            });
        return (
            <tr>
                <td style={borderStyle}>{this.props.entry.ranking}</td>
                <td style={borderStyle}>{this.props.entry.username}</td>
                <td style={borderStyle}>{this.props.entry.total_score}</td>
                {scores}
            </tr>
        );
    }
});

var RankingsTable = React.createClass({
    propTypes: {
        tournament: React.PropTypes.string.isRequired,
        entries:    React.PropTypes.array.isRequired,
        rounds:     React.PropTypes.number.isRequired
    },
    render: function() {

        var entries = this.props.entries.map(function(entry, idx) {
                return (
                    <EntryRow entry={entry} key={idx} />
                );
            }),
            longestEntry = {scores:[]};

        this.props.entries.forEach(function findEntryWithMostScores(entry) {
            if (entry.scores.length > longestEntry.scores.length) {
                longestEntry = entry;
            }
        });

        var scoreCategories = longestEntry.scores.map(function(cat, idx) {
            return (
                <td style={borderStyle} key={idx}>{cat.category}</td>
            );
        });

        return (
            <div>
                <p>Placings for {this.props.tournament}:</p>
    
                <table style={borderStyle}>

                    <thead>
                        <tr>
                            <td style={borderStyle}>Rank</td>
                            <td style={borderStyle}>Name</td>
                            <td style={borderStyle}>Total Score</td>
                            {scoreCategories}
                        </tr>
                    </thead>

                    <tbody>
                        {entries}
                    </tbody>
                </table>
            </div>
        );
    }
});

var TournamentRankingsPage = React.createClass({
    getInitialState: function () {
        return ({error: "", tournament: "", entries: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                if (!result.error && typeof result.entries !== "undefined" &&
                        result.entries.length === 0) {
                    this.setState({
                        error: "There are no players entered for this event"
                    });
                    return;
                }
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {

        var rankingsTable = <RankingsTable entries={this.state.entries}
                                tournament={this.state.tournament}
                                rounds={this.state.rounds || 5} />;

        return (
            <div>
                <p>{this.state.error}</p>
                {this.state.entries.length ? rankingsTable : null}
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentRankingsPage />,
    document.getElementById("content")
);
