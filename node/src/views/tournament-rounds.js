var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var InputWidget = React.createClass({
    getInitialState: function() {
        return {rounds: 5};
    },
    propTypes: {
        rounds: React.PropTypes.number,
        submitHandler: React.PropTypes.func.isRequired,
        tourn: React.PropTypes.string.isRequired
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
    handleChange: function(event) {
        this.setState({rounds: event.target.value});
    },
    render: function() {
        var tournText = this.props.tourn ?
                "for " + this.props.tourn + " here:"
                : "for a tournament on this page";

        return (
            <form onSubmit={this.props.submitHandler}>
                <p>Set the number of rounds {tournText}</p>
                
                <p>
                    <label htmlFor="rounds">Number of rounds:</label>
                    <input type="text"
                           value={this.state.rounds}
                           onChange={this.handleChange}
                           name="rounds"
                           id="rounds" />
                </p>
                <button type="submit">Set</button>
            </form>
        );
    }
});

var TournamentRoundsPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", tournament: "", rounds: 5});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            numRounds = $("input#rounds").val();

        $.post(window.location,
            {
                rounds: numRounds,
                tournament: this.state.tournament
            },
            function success(res) {
                _this.setState({successText: res.message, error: ""});
            })
            .fail(function (res) {
                _this.setState({error: res.responseJSON.message});
            });
    },
    render: function() {
        return (
            <div>
                <div>{this.state.successText}</div>
                <div>{this.state.error}</div>
                {
                    this.state.successText ?
                        null
                        : <InputWidget submitHandler={this.handleSubmit}
                                       tourn={this.state.tournament}
                                       rounds={this.state.rounds} />
                }
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentRoundsPage />,
    document.getElementById("content")
);
