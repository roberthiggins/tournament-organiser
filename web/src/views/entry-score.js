/* global $ React ReactDOM:true */
var Scores = require("./component-tournament-categories.js");

var EnterScoreForm = React.createClass({
    propTypes: {
        categories:          React.PropTypes.array.isRequired,
        submitHandler:       React.PropTypes.func.isRequired,
        gameId:              React.PropTypes.number
    },
    render: function() {
        if (!this.props.categories.length) {
            return <Scores.scoreCategoryWidget
                    categories={this.props.categories} />
        }

        return (
            <form onSubmit={this.props.submitHandler}>
                <div className="form_field">
                    <label htmlFor="value">Score:</label>
                    <input type="text" name="value" id="value" />
                </div>
                <Scores.scoreCategoryWidget
                    categories={this.props.categories} />
                <input type="hidden" name="gameId"
                    defaultValue={this.props.gameId} />
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
            success: false,
            categories: []
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
    handleSubmit: function (e) {
        e.preventDefault();

        $.post(window.location,
            $("form").serialize(),
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
                {this.state.success ?
                    null
                    : <EnterScoreForm submitHandler={this.handleSubmit}
                                      categories={this.state.categories}
                                      gameId={this.state.game_id} />}
            </div>
        );
    }
});


ReactDOM.render(
    <EnterScorePage />,
    document.getElementById("content")
);
