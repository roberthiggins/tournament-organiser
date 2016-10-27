var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Inputs = require("./component-inputs.js");

var RoundsForm = React.createClass({
    getInitialState: function() {
        return {rounds: null, tournament: ""};
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

        return (this.state.rounds !== null ?
            <form onSubmit={this.props.submitHandler}>
                <p>Set the number of rounds{tournText}</p>
                <p>
                    <Inputs.textField value={this.state.rounds}
                                      id="rounds"
                                      name="Number of rounds"
                                      changeHandler={this.handleRoundChange}/>
                </p>
                <button type="submit">Set</button>
            </form> :
            null);
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
                _this.setState(res.responseJSON);
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
