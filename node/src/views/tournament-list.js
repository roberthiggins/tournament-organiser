/* global $ React ReactDOM:true */
var TournamentList = React.createClass({
    getInitialState: function() {return ({tournaments: []});},
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
                <h2>Upcoming Tournaments:</h2>
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
