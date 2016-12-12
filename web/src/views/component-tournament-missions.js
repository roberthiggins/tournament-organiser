/* global React */

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
            <div className="form_field">
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.props.changeHandler}
                        value={this.props.val} />
            </div>);
    }
});

exports.missionField = MissionField;
