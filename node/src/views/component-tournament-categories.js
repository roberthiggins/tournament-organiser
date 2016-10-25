var React = require("react");

var EmptyCategory = function() {
    return {
        "name": "",
        "percentage": "",
        "per_tournament": false,
        "min_val": "",
        "max_val": "",
        "zero_sum": false,
        "opponent_score": false
    };
};

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
        categories: React.PropTypes.array.isRequired
    },
    render: function() {

        var displayElement = this.props.categories.length === 0 ?
            <p>No score categories available</p>
            : <div>
                <label htmlFor="key">Select a score category:</label>
                <select name="key" id="key">{this.props.categories}</select>
            </div>;

        return (displayElement);
    }
});

exports.emptyCategory = EmptyCategory;
exports.getCategories = getCategories;
exports.scoreCategoryWidget = ScoreCategories;
