var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Category = require("./component-tournament-categories.js");

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
            function (res) { this.setState(res); }.bind(this));
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

        $.post(window.location,
            {categories: this.state.categories},
            function success(res) {
                this.setState({successMsg: res.message, error: ""});
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
