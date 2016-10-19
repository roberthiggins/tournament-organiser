var React = require("react");

var RoundsWidget = React.createClass({
    propTypes: {
        rounds: React.PropTypes.oneOfType(
            [React.PropTypes.string, React.PropTypes.number]).isRequired,
        changeHandler: React.PropTypes.func.isRequired
    },
    render: function() {
        return (
            <p>
                <label htmlFor="rounds">Number of rounds:</label>
                <input type="text"
                       value={this.props.rounds}
                       onChange={this.props.changeHandler}
                       name="rounds"
                       id="rounds" />
            </p>
        );
    }
});

exports.roundsWidget = RoundsWidget;
