/* global React */

var Inputs = require("./component-inputs.js");

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

var handleCategoryStateChange = function(cats, event) {
    var idx = event.target.id.substr(0, 1),
        key = event.target.id.substr(2),
        chkbx = key.match(/per_tournament|zero_sum|opponent_score/);

    cats[idx][key] = chkbx ? event.target.checked : event.target.value;
    return cats;
};

// Input fields for defining a category in a form
var InputCategory = React.createClass({
    propTypes: {
        idx: React.PropTypes.number.isRequired,
        category: React.PropTypes.object.isRequired,
        changeHandler: React.PropTypes.func.isRequired
    },
    render: function() {
        return(<div className="category" key={this.props.idx + "_category"}>
            <Inputs.textField name={"Category " + (this.props.idx + 1)}
                              id={this.props.idx + "_name"}
                              changeHandler={this.props.changeHandler}
                              value={this.props.category.name }
                              key={this.props.idx + "_name"} />
            <Inputs.textField name="Percentage"
                              changeHandler={this.props.changeHandler}
                              id={this.props.idx + "_percentage"}
                              value={this.props.category.percentage }
                              key={this.props.idx + "_percentage"} />
            <Inputs.checkbox name="Once per tournament?"
                             changeHandler={this.props.changeHandler}
                             id={this.props.idx + "_per_tournament"}
                             checked={this.props.category.per_tournament }
                             key={this.props.idx + "_per_tournament"} />
            <Inputs.textField name="Min Score" id={this.props.idx + "_min_val"}
                              changeHandler={this.props.changeHandler}
                              value={this.props.category.min_val }
                              key={this.props.idx + "_min_val"} />
            <Inputs.textField name="Max Score"id={this.props.idx + "_max_val"}
                              changeHandler={this.props.changeHandler}
                              value={this.props.category.max_val }
                              key={this.props.idx + "_max_val"} />
            <Inputs.checkbox id={this.props.idx + "_zero_sum"}
                             changeHandler={this.props.changeHandler}
                             checked={this.props.category.zero_sum }
                             name="Zero Sum (score must be shared between game entrants)" />
            <Inputs.checkbox id={this.props.idx + "_opponent_score"}
                             changeHandler={this.props.changeHandler}
                             checked={this.props.category.opponent_score }
                             name="Opponent enters score" />
        </div>);
    }
});

// A list of 5 Category form widgets
var InputList = React.createClass({
    propTypes: {
        categories: React.PropTypes.array.isRequired,
        changeHandler: React.PropTypes.func.isRequired
    },
    render: function() {
        var widgets = this.props.categories
            .map(function(cat, idx) {
                return(<InputCategory category={cat}
                                      changeHandler={this.props.changeHandler}
                                      idx={idx}
                                      key={idx} />);
                }, this);

        return (
            <div className="categories">
                {widgets}
            </div>
        );
    }
});

// A widget for list score categories
var ScoreCategories = React.createClass({
    propTypes: {
        categories: React.PropTypes.array.isRequired
    },
    render: function() {

        var displayElement = this.props.categories.length === 0 ?
            <div>No score categories available</div>
            : <div>
                <label htmlFor="key">Select a score category:</label>
                <select name="key" id="key">{this.props.categories}</select>
            </div>;

        return (displayElement);
    }
});

exports.getCategories = getCategories;
exports.handleStateChange = handleCategoryStateChange;
exports.inputCategoryList = InputList;
exports.scoreCategoryWidget = ScoreCategories;
