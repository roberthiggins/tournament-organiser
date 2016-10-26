var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Inputs = require("./component-inputs.js");

var TournamentDetailsWidget = React.createClass({
    getInitialState: function() {
        return {rounds: 5};
    },
    propTypes: { handleSubmit: React.PropTypes.func.isRequired },
    handleRoundChange: function(event){
        this.setState({rounds: event.target.value});
    },
    render: function() {
        return (
            <form onSubmit={this.props.handleSubmit}>
                <p>
                    <label htmlFor="name">Tournament Name:</label>
                    <input type="text" name="name" id="name" />
                </p>

                <p>
                    <label htmlFor="date">Tournament Date:</label>
                    <input type="text" name="date" id="date" />
                </p>
                <p>
                    <Inputs.textField value={this.state.rounds}
                                      id="rounds"
                                      name="Number of rounds"
                                      changeHandler={this.handleRoundChange}/>
                </p>

                <button type="submit">Create</button>
            </form>
        );
    }
});

var SuccessWidget = React.createClass({
    propTypes: {
        name: React.PropTypes.string.isRequired,
        date: React.PropTypes.string.isRequired,
        rounds: React.PropTypes.oneOfType(
            [React.PropTypes.number, React.PropTypes.string])
    },
    render: function() {
        return (
            <div>
                <p>Tournament created! You submitted the following fields:</p>
                <ul>
                    <li>Name: {this.props.name}</li>
                    <li>Date: {this.props.date}</li>
                    {this.props.rounds ?
                        <li>Rounds: {this.props.rounds}</li> :
                        null}
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
            date = $("input#date").val(),
            rounds = $("input#rounds").val();

        $.post("/tournament/create",
            {
                name: name,
                date: date,
                rounds: rounds
            },
            function success() {
                _this.setState({
                    success: true,
                    date: date,
                    name: name,
                    rounds: rounds
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
                                   name={this.state.name}
                                   rounds={this.state.rounds} />
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
