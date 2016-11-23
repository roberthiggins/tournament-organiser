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
            <div className="form_field">
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.handleChange}
                        value={this.state.value} />
            </div>);
    }
});

var TournamentMissionsPage = React.createClass({
    getInitialState: function () {
        return ({error: "", message: "", missions: []});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState(result);
                }.bind(this))
            .fail(function(res) {
                this.setState(res.responseJSON);
                }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleSubmit: function (e) {
        e.preventDefault();

        var missions = $("form").serializeArray().map(function(input) {
            return input.value || "";
            });

        $.post(window.location, {missions: missions}, function success(res) {
            this.setState(res);
            }.bind(this));
    },
    render: function() {
        var missions = this.state.missions.map(function(mission, idx){
                return (
                    <MissionField name={"Round " + (idx + 1)}
                                  id={"missions_" + idx}
                                  val={mission}
                                  key={idx} />);
                }),
            form = missions.length ?
                <form onSubmit={this.handleSubmit}>
                    {missions}
                    <button type="submit">Set</button>
                </form>
                : null;

        return (
            <div>
                <h2>Missions</h2>
                {this.state.message ? <div>{this.state.message}</div> : null}
                {this.state.error ? <div>{this.state.error}</div> : null}
                {form}
            </div>
        );
    }
});


ReactDOM.render(
    <TournamentMissionsPage />,
    document.getElementById("content")
);
