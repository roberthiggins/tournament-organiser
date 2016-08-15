var React = require("react"),
    $ = require("jquery");

var getCategories = function(categories, perTournamentScores) {
    if (!categories) {
        return [];
    }

    return categories
        .filter(function(cat) {
            return perTournamentScores ?
                cat.per_tournament
                : !cat.per_tournament;
        })
        .map(function(cat, idx){
            return (
                <option value={cat.name} key={idx}>
                    {cat.name}
                </option>);
        });
};

// A widget for list score categories
var ScoreCategories = React.createClass({
    propTypes: {
        perTournamentScores: React.PropTypes.bool.isRequired
    },
    getInitialState : function(){
        return ({error: "", categories: []});
    },
    componentDidMount: function() {

        this.serverRequest = $.get(window.location + "/scorecategories",
            function (result) {
                if (result.error) {
                    this.setState(result);
                    return;
                }

                result.categories = getCategories(result.categories,
                    this.props.perTournamentScores);

                this.setState(result.categories.length < 1 ?
                    {error: "No score categories available"}
                    : result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {

        var displayElement = this.state.error ?
            <p>{this.state.error}</p>
            : <div>
                <label htmlFor="key">Select a score category:</label>
                <select name="key" id="key">
                    {this.state.categories}
                </select>
            </div>;

        return (displayElement);
    }
});

exports.scoreCategoryWidget = ScoreCategories;
