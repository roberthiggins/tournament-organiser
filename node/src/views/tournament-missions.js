/* global $ React ReactDOM:true */
var MissionField = React.createClass({
    getInitialState: function(){
        return {value: this.props.val};
    },
    propTypes: {
        id:   React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        val:  React.PropTypes.oneOfType(
                [React.PropTypes.string, React.PropTypes.number])
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
                        value={this.state.value} />
            </p>);
    }
});

var MissionForm = React.createClass({
    getInitialState: function () {
        return ({message: "", missions: []});
    },
    propTypes: {
        submitHandler: React.PropTypes.func.isRequired
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
    render: function() {
        var missions = this.state.missions.map(function(mission, idx){
                return (
                    <MissionField name={"Round " + (idx + 1)}
                                  id={"missions_" + idx}
                                  val={mission}
                                  key={idx} />);
            });
        if (!missions.length) {return null;}

        return (
            <form onSubmit={this.props.submitHandler}>
                {this.state.message ? <div>{this.state.message}</div> : null}
                {missions}
                <button type="submit">Set</button>
            </form>
        );
    }
});

var TournamentMissionsPage = React.createClass({
    getInitialState: function () {
        return ({message: ""});
    },
    handleSubmit: function (e) {
        e.preventDefault();
        var _this = this;

        $.post(window.location,
            $("form").serialize(),
            function success(res) {
                _this.setState(res);
            });
    },
    render: function() {
        return (
            <div>
                {this.state.message ?
                    <div>{this.state.message}</div> :
                    <MissionForm submitHandler={this.handleSubmit} />}
            </div>
        );
    }
});


ReactDOM.render(
    <TournamentMissionsPage />,
    document.getElementById("content")
);
