/* global $ React ReactDOM:true */
var Scores = require("./component-tournament-categories.js"),
    Inputs = require("./component-inputs");

var EnterScoreForm = React.createClass({
    propTypes: {
        categories:         React.PropTypes.array.isRequired,
        scoreChangeHandler: React.PropTypes.func.isRequired,
        score:              React.PropTypes.number,
        submitHandler:      React.PropTypes.func.isRequired,
    },
    render: function() {
        if (!this.props.categories.length) {
            return <Scores.scoreCategoryWidget
                    categories={this.props.categories} />;
        }

        return (
            <form onSubmit={this.props.submitHandler}>

                <Inputs.textField name="Score"
                                  id="value"
                                  changeHandler={this.props.scoreChangeHandler}
                                  value={this.props.score || ""} />
                <Scores.scoreCategoryWidget
                    categories={this.props.categories} />

                <button type="submit">Enter Score</button>
            </form>
        );
    }
});

var EnterScorePage = React.createClass({
    getInitialState: function () {
        return ({
            error: null,
            message: null,
            perTournament: false,
            score: null,
            success: false,
            categories: null
        });
    },
    componentDidMount: function() {

        this.contentRequest = $.get(window.location + "/content",
            function(contents) {

                this.setState(contents);

                this.categoryRequest = $.get(
                    window.location + "/scorecategories",
                    function (res) {
                        this.setState({
                            categories: Scores.getCategories(res.categories,
                                this.state.perTournament)
                            });
                    }.bind(this));

                }.bind(this));
    },
    componentWillUnmount: function() {
        this.contentRequest.abort();
        this.categoryRequest.abort();
    },
    handleScoreChange: function(event) {
        this.setState({score: event.target.value});
    },
    handleSubmit: function (e) {
        e.preventDefault();

        var data = {
            gameId: this.state.game_id,
            key: $("form select#key").find(":selected").text(),
            value: this.state.score,
            };

        $.post(window.location,
            data,
            function success(res) {
                this.setState({
                    error: null,
                    message: res.message,
                    success: true,
                    categories: []});
            }.bind(this))
            .fail(function (res) {
                this.setState(res.responseJSON);
            }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.error ?
                    <div>{this.state.error}</div>
                    : <div>{this.state.message}</div>}
                {this.state.success || this.state.categories === null ?
                    null
                    : <EnterScoreForm submitHandler={this.handleSubmit}
                                      categories={this.state.categories}
                                      scoreChangeHandler={this.handleScoreChange}
                                      score={this.state.score} />}
            </div>
        );
    }
});


ReactDOM.render(
    <EnterScorePage />,
    document.getElementById("content")
);
