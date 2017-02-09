/* global React */

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

var Select = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        options: React.PropTypes.array.isRequired,
        value: React.PropTypes.string
    },
    render: function() {
        var id = this.props.id,
            renderedOpts = this.props.options.map(function(opt, idx){
                return (
                    <option value={opt.val} key={idx}>
                        {opt.name}
                    </option>);
                });

        return (
            <div>
                <label htmlFor={id}>{this.props.name}:</label>
                <select name={id}
                        id={id}
                        onChange={this.props.changeHandler}
                        value={this.props.value}>
                    {renderedOpts}
                </select>
            </div>);
    }
});

var TextField = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        helpText: React.PropTypes.string,
        id: React.PropTypes.string.isRequired,
        name: React.PropTypes.string.isRequired,
        value: React.PropTypes.oneOfType(
                [React.PropTypes.string, React.PropTypes.number])
    },
    render: function() {
        var help = this.props.helpText ?
            <div className="helptext">{this.props.helpText}</div>
            : null;
        return (
            <div className="form_field">
                <label htmlFor={this.props.id}>{this.props.name}:</label>
                <input  type="text"
                        name={this.props.id}
                        id={this.props.id}
                        onChange={this.props.changeHandler}
                        value={this.props.value } />
                {help}
            </div>
        );
    }
});


exports.checkbox = Checkbox;
exports.select = Select;
exports.textField = TextField;
