var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var TournamentDetailsWidget = React.createClass({
    propTypes: { handleSubmit: React.PropTypes.func.isRequired },
    render: function() {
        return (
            <div>
                <form onSubmit={this.props.handleSubmit}>
                    <p>
                        <label htmlFor="name">Tournament Name:</label>
                        <input type="text" name="name" id="name" />
                    </p>

                    <p>
                        <label htmlFor="date">Tournament Date:</label>
                        <input type="text" name="date" id="date" />
                    </p>
                    <button type="submit">Create</button>
                </form>
            </div>
        );
    }
});

var SuccessWidget = React.createClass({
    propTypes: {
        name: React.PropTypes.string.isRequired,
        date: React.PropTypes.string.isRequired,
    },
    render: function() {
        return (
            <div>
                <p>Tournament created! You submitted the following fields:</p>
                <ul>
                    <li>Name: {this.props.name}</li>
                    <li>Date: {this.props.date}</li>
                </ul>
            </div>
        );
    }
});

var TournamentCreatePage = React.createClass({
    getInitialState: function () {
        return ({error: "", success: false});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            name = $("input#name").val(),
            date = $("input#date").val();

        $.post("/tournament/create", {name: name, date: date},
            function success() {
                _this.setState({
                    success: true,
                    date: date,
                    name: name
                });
            })
            .fail(function (res) {
                _this.setState({
                    success: false,
                    error: res.responseJSON.error
                });
            });
    },
    render: function() {
        return (
            <div>
                {this.state.success ?
                    <SuccessWidget date={this.state.date}
                                   name={this.state.name} />
                    : null
                }
                {this.state.success ?
                    null :
                    <p>You can add a tournament here</p>}
                {this.state.success ?
                    null :
                    <p>{this.state.error}</p>}
                {this.state.success ?
                    null :
                    <TournamentDetailsWidget handleSubmit={this.handleSubmit}/>}
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentCreatePage />,
    document.getElementById("content")
);
