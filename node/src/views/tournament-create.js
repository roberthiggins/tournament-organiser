var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery"),
    Inputs = require("./component-inputs.js");

var TournamentDetailsWidget = React.createClass({
    propTypes: {
        details: React.PropTypes.object.isRequired,
        handleRoundChange: React.PropTypes.func.isRequired,
        handleSubmit: React.PropTypes.func.isRequired
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
                    <Inputs.textField value={this.props.details.rounds}
                        id="rounds"
                        name="Number of rounds"
                        changeHandler={this.props.handleRoundChange}/>
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
        return ({
            details: {
                date: null,
                name: null,
                rounds: 5
                },
            error: "",
            success: false
            });
    },
    handleRoundChange: function(event){
        var details = this.state.details;
        details.rounds = event.target.value;
        this.setState({details: details});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var details = {
            name: $("input#name").val(),
            date: $("input#date").val(),
            rounds: this.state.details.rounds
            };

        $.post("/tournament/create",
            details,
            function success() {
                this.setState({
                    success: true,
                    details: details
                });
            }.bind(this))
            .fail(function (res) {
                this.setState({
                    success: false,
                    error: res.responseJSON.error
                });
            }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.success ?
                    <SuccessWidget date={this.state.details.date}
                                   name={this.state.details.name}
                                   rounds={this.state.details.rounds} />
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
                    <TournamentDetailsWidget details={this.state.details}
                        handleRoundChange={this.handleRoundChange}
                        handleSubmit={this.handleSubmit}/>}
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentCreatePage />,
    document.getElementById("content")
);
