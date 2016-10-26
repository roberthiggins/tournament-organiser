var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Inputs = require("./component-inputs.js"),
    Category = require("./component-tournament-categories.js");

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

var CategoriesForm = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        submitHandler: React.PropTypes.func.isRequired
    },
    getInitialState: function () {
        return ({message: "", categories: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                var numLines = 5,
                widgets = result.categories || [];
                while (result.categories.length < numLines) {
                    result.categories.push(Category.emptyCategory());
                }

                widgets = widgets.map(function(cat, idx) {
                    return(<div className="category" key={idx + "_category"}>
                        <Inputs.textField name="Category" id={idx + "_name"}
                              changeHandler={this.props.changeHandler}
                              val={cat.name }
                              key={idx + "_name"} />
                        <Inputs.textField name="Percentage"
                              changeHandler={this.props.changeHandler}
                              id={idx + "_percentage"}
                              val={cat.percentage }
                              key={idx + "_percentage"} />
                        <ScoreCheckbox name="Once per tournament?"
                                       id={idx + "_per_tournament"}
                                       checked={cat.per_tournament }
                                       key={idx + "_per_tournament"} />
                        <Inputs.textField name="Min Score" id={idx + "_min_val"}
                              changeHandler={this.props.changeHandler}
                              val={cat.min_val }
                              key={idx + "_min_val"} />
                        <Inputs.textField name="Max Score"id={idx + "_max_val"}
                              changeHandler={this.props.changeHandler}
                              val={cat.max_val }
                              key={idx + "_max_val"} />
                        <ScoreCheckbox id={idx + "_zero_sum"}
                                       checked={cat.zero_sum }
                                       name="Zero Sum (score must be shared between game entrants)" />
                        <ScoreCheckbox id={idx + "_opponent_score"}
                                       checked={cat.opponent_score }
                                       name="Opponent enters score" />
                    </div>);
                }.bind(this));


                result.categories = widgets;
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler}>
                {this.state.message ? <div>{this.state.message}</div> : null}
                {this.state.categories}
                <button type="submit">Set</button>
            </form>
        );
    }
});

var TournamentCategoriesPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successMsg: ""});
    },
    handleChange: function(event) {
        var cats = this.state.categories,
            idx = event.target.id.substr(0, 1),
            key = event.target.id.substr(2),
            chkbx = key.match(/per_tournament|zero_sum|opponent_score/);

        cats[idx][key] = chkbx ? event.target.checked : event.target.value;
        this.setState({categories: cats});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var categories = [];

        try {
            $("form div.category").each(function() {
                var serialized = serializeCategory($(this));
                if (serialized) {
                    categories.push(serialized);
                }
            });
        }
        catch (err) {
            this.setState({error: err});
            return;
        }

        $.post(window.location,
            {categories: categories},
            function success(res) {
                this.setState({successMsg: res.message});
            }.bind(this))
            .fail(function (res) {
                this.setState(res);
            }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.error ? <div>{this.state.error}</div> : null}
                {this.state.successMsg ?
                    <div>{this.state.successMsg}</div> :
                    <CategoriesForm changeHandler={this.handleChange}
                                    submitHandler={this.handleSubmit} />}
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentCategoriesPage />,
    document.getElementById("content")
);
