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

        var tournaments = this.state.tournaments.map(function(trn, idx) {
                return (
                    <li key={idx}>
                        <a href={"/tournament/" + trn.name}>
                            {trn.name}
                        </a>
                        {trn.user_entered ? <strong> Entered </strong> : null}
                         - Date: {trn.date}, Confirmed Entries: {trn.entries}
                    </li>
                );
            }),
            tournList = this.state.tournaments.length ?
                <ul>
                    {tournaments}
                </ul>
                : <p>There are no upcoming tournaments</p>;

        return (
            <div>
                <h2>Upcoming Tournaments:</h2>
                {tournList}
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentList />,
    document.getElementById("content")
);
