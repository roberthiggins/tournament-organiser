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
                <p>
                    <label htmlFor="name">Tournament Name:</label>
                    <input type="text" name="name" id="name" />
                </p>

                <p>
                    <label htmlFor="date">Tournament Date:</label>
                    <input type="text" name="date" id="date" />
                </p>
                <p>
                    <Inputs.textField value={this.props.details.rounds}
                        id="rounds"
                        name="(Optional) Number of rounds"
                        changeHandler={this.props.handleRoundChange}/>
                </p>
                <p>(Optional) Add Score Categories:</p>
                <CategoryComponent.inputCategoryList
                    changeHandler={this.props.handleCategoryChange}
                    categories={this.props.details.categories}/>
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
            : null;
        return (
            <div>
                <p>Tournament created! You submitted the following fields:</p>
                <ul>
                    <li>Name: {this.props.details.name}</li>
                    <li>Date: {this.props.details.date}</li>
                    {this.props.details.rounds ?
                        <li>Rounds: {this.props.details.rounds}</li> :
                        null}
                    {this.props.details.categories ?
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
        var details = {
            categories: this.state.details.categories,
            name: $("input#name").val(),
            date: $("input#date").val(),
            rounds: this.state.details.rounds
            };

        $.post("/tournament/create",
            details,
            function success() {
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
                    <p>You can add a tournament here</p>}
                {this.state.success ?
                    null :
                    <p>{this.state.error}</p>}
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
