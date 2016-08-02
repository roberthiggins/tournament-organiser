var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var ScoreField = React.createClass({
    getInitialState: function() {
        return {value: ""};
    },
    handleChange: function(event) {
        this.setState({value: event.target.value});
    },
    propTypes: {
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        type: React.PropTypes.string.isRequired,
        val: React.PropTypes.any
    },
    render: function() {
        return (
            <span>
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type={this.props.type}
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.handleChange}
                        value={this.state.value || this.props.val} />
            </span>
        );
    }
});

var Category = React.createClass({
    propTypes: {
        idx: React.PropTypes.number.isRequired,
        vals: React.PropTypes.object.isRequired
    },
    render: function() {
        return (
            <div className="category">
                <ScoreField type="text" name="Category"
                            id={this.props.idx + "_name"}
                            val={this.props.vals.name} />
                <ScoreField type="text" name="Percentage"
                            id={this.props.idx + "_percentage"}
                            val={this.props.vals.percentage} />
                <ScoreField type="checkbox" name="Once per tournament?"
                            id={this.props.idx + "_per_tournament"}
                            checked={this.props.vals.per_tournament} />
                <ScoreField type="text" name="Min Score"
                            id={this.props.idx + "_min_val"}
                            val={this.props.vals.min_val} />
                <ScoreField type="text" name="Max Score"
                            id={this.props.idx + "_max_val"}
                            val={this.props.vals.max_val} />
            </div>
        );
    }
});

var InputWidget = React.createClass({
    propTypes: {
        categories: React.PropTypes.array,
        submitHandler: React.PropTypes.func.isRequired
    },
    render: function() {

        var numLines = 5,
            lastIdx = 0,
            categoryFields = this.props.categories.map(function(cat, idx) {
                lastIdx = idx;
                return (<Category vals={cat} idx={idx} key={idx} />);
            }),
            emptyCats = { name: "", percentage: "", per_tournament: "",
                min_val: "", max_val: ""};
        while (categoryFields.length < numLines) {
            lastIdx = lastIdx + 1;
            categoryFields.push(
                <Category vals={emptyCats} idx={lastIdx} key={lastIdx} />);
        }

        return (
            <form onSubmit={this.props.submitHandler}>
                {categoryFields}
                <button type="submit">Set</button>
            </form>
        );
    }
});

var serializeCategory = function($categoryDiv) {
    var elementsAsDictionaries = $categoryDiv
            .find(":input:text[value!=''],:input:checkbox:checked")
            .serializeArray()
            .map(function(dict) {
                // We can strip the index from the front of the name as it
                // was only there for display help and convert checkboxes
                // to true
                return {
                    name: dict.name.substr(2),
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

    return categoryValues;
};


var TournamentCategoriesPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", tournament: "", categories: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
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

        $("form div.category").each(function() {
            var serialized = serializeCategory($(this));
            if (serialized.length === 5) {
                categories.push(serialized);
            }
        });

        $.post(window.location,
            {categories: categories},
            function success(res) {
                _this.setState(
                    {successText: res.message, error: "", message: ""});
            })
            .fail(function (res) {
                _this.setState({error: res.responseJSON.message});
            });
    },
    render: function() {
        return (
            <div>

                <div>{this.state.successText}</div>
                <div>{this.state.error}</div>
                <div>{this.state.message}</div>
                {
                    this.state.successText ?
                        null
                        : <InputWidget submitHandler={this.handleSubmit}
                                       categories={this.state.categories} />
                }
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentCategoriesPage />,
    document.getElementById("content")
);
