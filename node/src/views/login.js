var React = require('react'),
    ReactDOM = require('react-dom');

var InputField = React.createClass({
    propTypes: {
        name:    React.PropTypes.string.isRequired,
        display: React.PropTypes.string.isRequired,
        type:    React.PropTypes.string.isRequired
    },
    render: function() {
        return (
            <p>
                <label htmlFor={this.props.name}>
                    {this.props.display}:
                </label>
                <input type={this.props.type} name={this.props.name}
                       id={this.props.name} />
            </p>
        );
    }
});

var LoginWidget = React.createClass({
    render: function() {
        return (
            <div>
                <form method="POST" action="">
                    <p>Login to your account</p>
                    <InputField display="Username" name="username"
                                type="text" />
                    <InputField display="Password" name="password"
                                type="password" />
                    <button type="submit">Login</button>
                </form>
                <p>
                    <a href="/resetpassword">Forgot Password</a>
                </p>
                <p>
                    <a href="/signup">Create Account</a>
                </p>
            </div>
        );
    }
});

ReactDOM.render(
    <LoginWidget />,
    document.getElementById('content')
);
