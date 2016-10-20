var React = require("react");


var MissionField = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        id:   React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        val:  React.PropTypes.oneOfType(
                [React.PropTypes.string, React.PropTypes.number])
    },
    render: function() {
        return (
            <p>
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.props.changeHandler}
                        value={this.props.val} />
            </p>);
    }
});

exports.missionField = MissionField;
