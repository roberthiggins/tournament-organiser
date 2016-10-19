var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Round = require("./component-set-rounds.js");

var RoundsForm = React.createClass({
    getInitialState: function() {
        return {rounds: 5, tournament: ""};
    },
    propTypes: {
        submitHandler: React.PropTypes.func.isRequired
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
    handleRoundChange: function(event) {
        this.setState({rounds: event.target.value});
    },
    render: function() {
        var tournText = this.state.tournament ?
                " for " + this.state.tournament + " here:"
                : " here:";

        return (
            <form onSubmit={this.props.submitHandler}>
                <p>Set the number of rounds{tournText}</p>
                <Round.roundsWidget rounds={this.state.rounds}
                                    changeHandler={this.handleRoundChange}/>
                <button type="submit">Set</button>
            </form>
        );
    }
});

var TournamentRoundsPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: ""});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            numRounds = $("input#rounds").val();

        $.post(window.location,
            {rounds: numRounds},
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
                        : <RoundsForm submitHandler={this.handleSubmit} />
                }
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentRoundsPage />,
    document.getElementById("content")
);
