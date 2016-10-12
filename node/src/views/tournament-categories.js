var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var ScoreField = React.createClass({
    getInitialState: function() {
        return {value: this.props.val};
    },
    handleChange: function(event) {
        this.setState({value: event.target.value});
    },
    propTypes: {
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        val: React.PropTypes.oneOfType(
                [React.PropTypes.string, React.PropTypes.number])
    },
    render: function() {
        return (
            <span>
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.handleChange}
                        value={this.state.value } />
            </span>
        );
    }
});

var ScoreCheckbox = React.createClass({
    getInitialState: function() {
        return {checked: this.props.checked};
    },
    handleChange: function(event) {
        this.setState({checked: event.target.checked});
    },
    propTypes: {
        checked: React.PropTypes.bool.isRequired,
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
    },
    render: function() {
        return (
            <span>
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="checkbox"
                        name={this.props.id}
                        id={this.props.id}
                        checked={this.state.checked}
                        onChange={this.handleChange} />
            </span>
        );
    }
});

var serializeCategory = function($categoryDiv) {
    var category = {},
        requiredFields = ["name", "percentage", "min_val", "max_val"],
        serialized = $categoryDiv
                        .find(":input:text[value!=''],:input:checkbox:checked")
                        .serializeArray();
    if (!serialized.length) {
        return null;
    }

    serialized.forEach(function(dict) {
        // We can strip the index from the front of the name as it
        // was only there for display help and convert checkboxes
        // to true
        category[dict.name.substr(2)] = dict.value === "on" ? true : dict.value;
    });

    requiredFields.forEach(function(key){
        if ((category[key] || "") === "") {
            throw "Please fill in all fields";
        }
    });

    // Checkboxes won't be serialized if false
    category["per_tournament"] = category["per_tournament"] || false;
    category["zero_sum"] = category["zero_sum"] || false;
    category["opponent_score"] = category["opponent_score"] || false;

    return category;
};

var category = function(idx, name, pct, per_tournament, min_val, max_val,
                        zero_sum, opp_score) {
    return (
        <div className="category" key={idx + "_category"}>
            <ScoreField name="Category" id={idx + "_name"} val={name}
                        key={idx + "_name"} />
            <ScoreField name="Percentage" id={idx + "_percentage"} val={pct}
                        key={idx + "_percentage"} />
            <ScoreCheckbox name="Once per tournament?"
                           id={idx + "_per_tournament"}
                           checked={per_tournament}
                           key={idx + "_per_tournament"} />
            <ScoreField name="Min Score" id={idx + "_min_val"} val={min_val}
                        key={idx + "_min_val"} />
            <ScoreField name="Max Score"id={idx + "_max_val"} val={max_val}
                        key={idx + "_max_val"} />
            <ScoreCheckbox id={idx + "_zero_sum"} checked={zero_sum}
                           name="Zero Sum (score must be shared between game entrants)" />
            <ScoreCheckbox id={idx + "_opponent_score"} checked={opp_score}
                           name="Opponent enters score" />
        </div>
        );
};

var TournamentCategoriesPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", tournament: "", categories: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                var numLines = 5,
                    lastIdx = -1,
                    widgets = [];

                if (result.categories) {
                    widgets = result.categories.map(function(cat, idx) {
                        lastIdx = idx;
                        return category(idx, cat.name, cat.percentage,
                            cat.per_tournament, cat.min_val, cat.max_val,
                            cat.zero_sum, cat.opponent_score);
                    });
                }
                while (widgets.length < numLines) {
                    lastIdx = lastIdx + 1;
                    widgets.push(
                        category(lastIdx, "", "", false, "", "", false, false));
                }

                result.categories = widgets;
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            categories = [];

        try {
            $("form div.category").each(function() {
                var serialized = serializeCategory($(this));
                if (serialized) {
                    categories.push(serialized);
                }
            });
        }
        catch (err) {
            _this.setState({error: err});
            return;
        }

        $.post(window.location,
            {categories: categories},
            function success(res) {
                _this.setState(
                    {successText: res.message, error: "", message: ""});
            })
            .fail(function (res) {
                _this.setState({error: res.responseJSON.error});
            });
    },
    render: function() {
        return (
            <div>

                <p>{this.state.successText}</p>
                <p>{this.state.error}</p>
                <p>{this.state.message}</p>
                {this.state.successText ? null:
                    <form onSubmit={this.handleSubmit}>
                        {this.state.categories}
                        <button type="submit">Set</button>
                    </form>}
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentCategoriesPage />,
    document.getElementById("content")
);
