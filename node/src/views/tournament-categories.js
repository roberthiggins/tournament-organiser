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

var Category = React.createClass({
    propTypes: {
        idx: React.PropTypes.number.isRequired,
        vals: React.PropTypes.object
    },
    getDefaultProps: function(){
        return {
            vals: {name: "", percentage: "", per_tournament: false,
                   min_val: "", max_val: ""}
        };
    },
    render: function() {
        return (
            <div className="category">
                <ScoreField name="Category"
                            id={this.props.idx + "_name"}
                            val={this.props.vals.name} />
                <ScoreField name="Percentage"
                            id={this.props.idx + "_percentage"}
                            val={this.props.vals.percentage} />
                <ScoreCheckbox name="Once per tournament?"
                               id={this.props.idx + "_per_tournament"}
                               checked={this.props.vals.per_tournament} />
                <ScoreField name="Min Score"
                            id={this.props.idx + "_min_val"}
                            val={this.props.vals.min_val} />
                <ScoreField name="Max Score"
                            id={this.props.idx + "_max_val"}
                            val={this.props.vals.max_val} />
            </div>
        );
    }
});
Category.serialize = function($categoryDiv) {
    var elementsAsDictionaries = $categoryDiv
            .find(":input:text[value!=''],:input:checkbox:checked")
            .serializeArray()
            .map(function(dict) {
                // We can strip the index from the front of the name as it
                // was only there for display help and convert checkboxes
                // to true
                return {
                    key: dict.name.substr(2),
                    value: dict.value === "on" ? true : dict.value
                };
            }),
        categoryValues = [];

    elementsAsDictionaries.forEach(function(elem, idx) {
        if (idx === 2 && elem.key !== "per_tournament") {
            // This should be a checkbox. If not we shim one in.
            categoryValues.push(false);
        }

        categoryValues.push(elem.value);
    });

    if (categoryValues.length !== 5 && categoryValues.length !== 0) {
        return null;
    }

    return {
        "name": categoryValues[0],
        "percentage": categoryValues[1],
        "per_tourn": categoryValues[2],
        "min_val": categoryValues[3],
        "max_val": categoryValues[4]
        };
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
                        return (<Category vals={cat} idx={idx} key={idx} />);
                    });
                }
                while (widgets.length < numLines) {
                    lastIdx = lastIdx + 1;
                    widgets.push(<Category idx={lastIdx} key={lastIdx} />);
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
            categories = [],
            error = false;

        $("form div.category").each(function() {
            var serialized = Category.serialize($(this));
            if (!serialized) {
                _this.setState({error: "Please fill in all fields"});
                error = true;
                return;
            }
            categories.push(serialized);
        });

        if (error) {
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
