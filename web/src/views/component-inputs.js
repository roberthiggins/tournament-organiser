var React = require("react");

var Checkbox = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        checked: React.PropTypes.bool.isRequired,
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
    },
    render: function() {
        return (
            <div className="form_field">
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="checkbox"
                        name={this.props.id}
                        id={this.props.id}
                        checked={this.props.checked}
                        onChange={this.props.changeHandler} />
            </div>
        );
    }
});

var TextField = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        value: React.PropTypes.oneOfType(
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
                        value={this.props.value } />
            </div>
        );
    }
});


exports.checkbox = Checkbox;
exports.textField = TextField;
