/* global $ React ReactDOM:true */
var Inputs = require("./component-inputs");

var EnterScoreForm = React.createClass({
    propTypes: {
        categories:         React.PropTypes.array.isRequired,
        scoreChangeHandler: React.PropTypes.func.isRequired,
        score:              React.PropTypes.number,
        submitHandler:      React.PropTypes.func.isRequired,
    },
    render: function() {
        if (!this.props.categories.length) {
            return <div>"No score categories available"</div>;
        }

        return (
            <form onSubmit={this.props.submitHandler}>

                <Inputs.textField name="Score"
                                  id="score"
                                  changeHandler={this.props.scoreChangeHandler}
                                  value={this.props.score || ""} />
                <Inputs.select id="category"
                               name="Select a score category"
                               options={this.props.categories} />

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

                        var cats = res.categories.filter(function(cat) {
                                return this.state.perTournament ?
                                    cat.per_tournament
                                    : !cat.per_tournament;
                                }.bind(this));

                        this.setState({categories: cats});
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
            category: $("form select#category").find(":selected").text(),
            score: this.state.score,
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
