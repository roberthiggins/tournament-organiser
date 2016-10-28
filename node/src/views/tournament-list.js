var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var TournamentList = React.createClass({
    getInitialState: function() {return ({tournaments: []});},
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState({tournaments: JSON.parse(result).tournaments});
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {

        var tournList = this.state.tournaments.map(function(tournament, idx) {
            return (
                <li key={idx}>
                    <a href={"/tournament/" + tournament.name}>
                        {tournament.name} - {tournament.date}
                    </a>
                </li>
            );
        });

        return (
            <div>
                <p>See available tournaments below:</p>
                <ul>
                    {tournList}
                </ul>
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentList />,
    document.getElementById("content")
);