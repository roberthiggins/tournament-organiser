/* global $ React ReactDOM:true */
var scores = require("./component-tournament-categories.js");

var EnterScoreForm = React.createClass({
    propTypes: {
        categories:          React.PropTypes.array.isRequired,
        submitHandler:       React.PropTypes.func.isRequired,
        gameId:              React.PropTypes.number
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler}>
                <p>
                    <label htmlFor="value">Score:</label>
                    <input type="text" name="value" id="value" />
                </p>
                <scores.scoreCategoryWidget
                    categories={this.props.categories} />
                <input type="hidden" name="gameId" defaultValue={this.props.gameId} />
                <button type="submit">Enter Score</button>
            </form>
        );
    }
});

var EnterScorePage = React.createClass({
    getInitialState: function () {
        return ({
            error: "",
            successText: "",
            perTournament: false,
            categories: []
        });
    },
    componentDidMount: function() {

        var getContent = function(result) {
                this.setState(result);
            }.bind(this),
            getCategories = function() {
                this.categoryRequest = $.get(
                    window.location + "/scorecategories",
                    function (result) {
                        if (result.error) {
                            this.setState(result);
                            return;
                        }

                        var categories = scores.getCategories(
                                result.categories,
                                this.state.perTournament);

                        this.setState({categories: categories});
                    }.bind(this));
            }.bind(this);

        this.contentRequest = $.get(window.location + "/content", getContent)
            .done(getCategories);
    },
    componentWillUnmount: function() {
        this.contentRequest.abort();
    },
    handleSubmit: function (e) {
        e.preventDefault();
        var _this = this;

        $.post(window.location,
            $("form").serialize(),
            function success(res) {
                _this.setState({successText: res.message, error: "",
                    message: "", categories: []});
            })
            .fail(function (res) {
                _this.setState(res.responseJSON);
            });
    },
    render: function() {

        var widget = null,
            showMessage = true;
        if (this.state.error) {
            showMessage = false;
            widget = <div>{this.state.error}</div>;
        }
        else if (this.state.successText) {
            showMessage = false;
            widget = <div>{this.state.successText}</div>;
        }
        else if (this.state.categories.length === 0) {
            showMessage = false;
            widget = <div>No score categories available</div>;
        }
        else {
            widget = <EnterScoreForm submitHandler={this.handleSubmit}
                categories={this.state.categories}
                gameId={this.state.game_id} />;
        }

        return (
            <div>
                {showMessage ? <div>{this.state.message}</div> : null}
                {widget}
            </div>
        );
    }
});


ReactDOM.render(
    <EnterScorePage />,
    document.getElementById("content")
);
