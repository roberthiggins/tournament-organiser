var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var Entries = React.createClass({
    propTypes: {
        entries: React.PropTypes.array.isRequired
    },
    render: function() {
        var entries = this.props.entries.map(function(entry, idx) {
            return(<li key={idx}>{entry}</li>);
        });
        return (
            <div>
                <p>Entries:</p>
                <ol>
                    {entries}
                </ol>
            </div>
        );
    }
});

var TournamentEntriesPage = React.createClass({
    getInitialState: function () {
        return ({tournament: "", entries: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState(result);
            }.bind(this))
            .fail(function(res){
                this.setState({message: res.responseJSON.error});
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        var registerURL = "/tournament/" + this.state.tournament + "/register";
        return (
            <div>
                <p>{this.state.message}</p>
                {this.state.tournament && !this.state.entries.length ?
                    <p>
                        There are no entries yet.
                        { " " }
                        <a href={registerURL}>Be the first!</a>
                    </p>
                    : null
                }
                {this.state.entries.length ?
                    <Entries entries={this.state.entries} /> : null} 
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentEntriesPage />,
    document.getElementById("content")
);

