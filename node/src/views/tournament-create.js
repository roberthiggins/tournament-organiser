/* global $ React ReactDOM:true */
var CategoryComponent = require("./component-tournament-categories.js"),
    CategoryModel = require("../models/score-categories.js"),
    Inputs = require("./component-inputs.js");

var TournamentDetailsWidget = React.createClass({
    propTypes: {
        details: React.PropTypes.object.isRequired,
        handleCategoryChange: React.PropTypes.func.isRequired,
        handleRoundChange: React.PropTypes.func.isRequired,
        handleSubmit: React.PropTypes.func.isRequired
    },
    render: function() {
        return (
            <form onSubmit={this.props.handleSubmit}>
                <div>
                    <label htmlFor="name">Tournament Name:</label>
                    <input type="text" name="name" id="name" />
                </div>

                <div>
                    <label htmlFor="date">Tournament Date:</label>
                    <input type="text" name="date" id="date" />
                </div>
                <div>
                    <Inputs.textField value={this.props.details.rounds}
                        id="rounds"
                        name="(Optional) Number of rounds"
                        changeHandler={this.props.handleRoundChange}/>
                </div>
                <div>
                    <div>(Optional) Add Score Categories:</div>
                    <CategoryComponent.inputCategoryList
                        changeHandler={this.props.handleCategoryChange}
                        categories={this.props.details.categories}/>
                </div>
                <button type="submit">Create</button>
            </form>
        );
    }
});

var SuccessWidget = React.createClass({
    propTypes: {
        details: React.PropTypes.object.isRequired
    },
    render: function() {
        var categories = this.props.details.categories ?
            this.props.details.categories.map(function(cat){return cat.name})
            : [];
        return (
            <div>
                <div>Tournament created! You submitted the following fields:</div>
                <ul>
                    <li>Name: {this.props.details.name}</li>
                    <li>Date: {this.props.details.date}</li>
                    {this.props.details.rounds ?
                        <li>Rounds: {this.props.details.rounds}</li> :
                        null}
                    {categories.length ?
                        <li>Score Categories: {categories.join(", ")}</li>
                        : null}
                </ul>
            </div>
        );
    }
});

var TournamentCreatePage = React.createClass({
    getInitialState: function () {
        return ({
            details: {
                categories: [CategoryModel.emptyScoreCategory(),
                             CategoryModel.emptyScoreCategory(),
                             CategoryModel.emptyScoreCategory()],
                date: null,
                name: null,
                rounds: 5
                },
            error: "",
            success: false
            });
    },
    handleCategoryChange: function(event) {
        var details = this.state.details;
        details.categories = CategoryComponent.handleStateChange(
            this.state.details.categories, event)
        this.setState({details: details});
    },
    handleRoundChange: function(event){
        var details = this.state.details;
        details.rounds = event.target.value;
        this.setState({details: details});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();

        $.post("/tournament/create",
            {
                categories: this.state.details.categories,
                name: $("input#name").val(),
                date: $("input#date").val(),
                rounds: this.state.details.rounds
            },
            function success(res) {
                var details = res;
                if (res.score_categories) {
                    res.categories = res.score_categories;
                    delete res.score_categories;
                }
                this.setState({
                    success: true,
                    details: details
                });
            }.bind(this))
            .fail(function (res) {
                this.setState({
                    success: false,
                    error: res.responseJSON.error
                });
            }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.success ?
                    <SuccessWidget details={this.state.details} />
                    : null}
                {this.state.success ?
                    null :
                    <div>
                        <h2>You can add a tournament here</h2>
                    </div>}
                {this.state.success ?
                    null :
                    <div>{this.state.error}</div>}
                {this.state.success ?
                    null :
                    <TournamentDetailsWidget details={this.state.details}
                        handleCategoryChange={this.handleCategoryChange}
                        handleRoundChange={this.handleRoundChange}
                        handleSubmit={this.handleSubmit}/>}
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentCreatePage />,
    document.getElementById("content")
);
