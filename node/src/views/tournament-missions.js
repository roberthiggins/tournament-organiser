var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");


var MissionField = React.createClass({
    getInitialState: function(){ return {value: ""}; },
    propTypes: {
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        val: React.PropTypes.string
    },
    handleChange: function(event) {
        this.setState({value: event.target.value});
    },
    render: function() {
        return (
            <p>
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.handleChange}
                        value={this.state.value || this.props.val} />
            </p>);
    }
});

var MissionForm = React.createClass({
    propTypes: {
        missions: React.PropTypes.array.isRequired,
        submitHandler: React.PropTypes.func.isRequired
    },
    render: function() {
        var missions = this.props.missions.map(function(mission, idx){
                return (
                    <MissionField name={"Round " + (idx + 1)}
                                  id={"missions_" + idx}
                                  val={mission}
                                  key={idx} />);
            });


        return (
            <form onSubmit={this.props.submitHandler}>
                {missions}
                <button type="submit">Set</button>
            </form>
        );
    }
});

var TournamentMissionsPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", tournament: "", missions: []});
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
        e.preventDefault();
        var _this = this;

        $.post(window.location,
            $("form").serialize(),
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
                        : <MissionForm submitHandler={this.handleSubmit}
                                       missions={this.state.missions} />
                }
            </div>
        );
    }
});



ReactDOM.render(
    <TournamentMissionsPage />,
    document.getElementById("content")
);
