/* global $ React ReactDOM:true */
var Category = require("./component-tournament-categories.js");

var TournamentCategoriesPage = React.createClass({
    getInitialState: function () {
        return ({error: "", instructions: "", successMsg: "", categories: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function(res) {
                this.setState(res);
                }.bind(this))
            .fail(function(res) {
                this.setState(res.responseJSON);
                }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleChange: function(event) {
        this.setState({
            categories: Category.handleStateChange(this.state.categories, event)
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

        var widget = this.state.successMsg ?
            <div>{this.state.successMsg}</div> :
            <form onSubmit={this.handleSubmit}>
                <div>{this.state.instructions}</div>
                {this.state.categories.length ?
                    <Category.inputCategoryList
                        changeHandler={this.handleChange}
                        categories={this.state.categories}/> :
                    null}
                <button type="submit">Set</button>
            </form>;
        return (
            <div>
                <h2>Score Categories</h2>
                {this.state.error ? <div>{this.state.error}</div> : widget}
            </div>
        );
    }
});


ReactDOM.render(
    <TournamentCategoriesPage />,
    document.getElementById("content")
);
