var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Category = require("./component-tournament-categories.js");

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

var handleCategoryStateChange = function(cats, event) {
    var idx = event.target.id.substr(0, 1),
        key = event.target.id.substr(2),
        chkbx = key.match(/per_tournament|zero_sum|opponent_score/);

    cats[idx][key] = chkbx ? event.target.checked : event.target.value;
    return cats;
};

var TournamentCategoriesPage = React.createClass({
    getInitialState: function () {
        return ({error: "", instructions: "", successMsg: "", categories: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (res) {
                this.setState({
                    categories: res.categories,
                    instructions: res.message
                    });
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleChange: function(event) {
        this.setState({
            categories: handleCategoryStateChange(this.state.categories, event)
            });
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
            this.setState({error: ""});
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
                this.setState({error: res.responseJSON.error});
            }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.error ? <div>{this.state.error}</div> : null}
                {this.state.successMsg ?
                    <div>{this.state.successMsg}</div> :
                    <form onSubmit={this.handleSubmit}>
                        <div>{this.state.instructions}</div>
                        {this.state.categories.length ?
                            <Category.inputCategoryList
                                changeHandler={this.handleChange}
                                categories={this.state.categories}/> :
                            null}
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

exports.categoriesHandleStateChange = handleCategoryStateChange;
