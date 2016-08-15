var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    scores = require("./component-tournament-categories.js");

var EnterScoreForm = React.createClass({
    propTypes: {
        submitHandler:       React.PropTypes.func.isRequired,
        perTournamentScores: React.PropTypes.bool.isRequired
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler}>
                <p>
                    <label htmlFor="value">Score:</label>
                    <input type="text" name="value" id="value" />
                </p>
                <scores.scoreCategoryWidget
                    perTournamentScores={this.props.perTournamentScores} />
                <button type="submit">Enter Score</button>
            </form>
        );
    }
});

var EnterScorePage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", perTournament: false});
    },
    componentDidMount: function() {

        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                if (result.error) {
                    this.setState({successText : result.error});
                    return;
                }
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleSubmit: function (e) {
        e.preventDefault();
        var _this = this;

        $.post(window.location,
            $("form").serialize(),
            function success(res) {
                _this.setState(
                    {successText: res.message, error: "", message: ""});
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
                <div>{this.state.message}</div>
                {
                    this.state.successText ?
                        null
                        : <EnterScoreForm submitHandler={this.handleSubmit}
                            perTournamentScores={this.state.perTournament} />
                }
            </div>
        );
    }
});


ReactDOM.render(
    <EnterScorePage />,
    document.getElementById("content")
);
