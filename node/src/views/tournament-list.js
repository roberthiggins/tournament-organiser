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

        var tournList = this.state.tournaments.map(function(tourn, idx) {
            return (
                <li key={idx}>
                    <a href={"/tournament/" + tourn.name}>
                        {tourn.name}
                    </a>
                     - Date: {tourn.date}, Confirmed Entries: {tourn.entries}
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
