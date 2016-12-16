/* global $ React ReactDOM:true */
var SignupForm = React.createClass({
    propTypes: {
        submitHandler: React.PropTypes.func,
        error: React.PropTypes.string
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler}>
                <h2>You can add/change your details here:</h2>

                <div>{this.props.error}</div>

                <div className="form_field">
                    <label htmlFor="username">Username:</label>
                    <input type="text" name="username" maxLength="30"
                           id="username" />
                    <div className="helptext">Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.</div>
                </div>

                <div className="form_field">
                    <label htmlFor="email">Email:</label>
                    <input type="email" name="email" id="email" />
                </div>

                <div className="form_field">
                    <label htmlFor="password1">Password:</label>
                    <input type="password" name="password1" id="password1" />
                </div>

                <div className="form_field">
                    <label htmlFor="password2">Password confirmation:</label>
                    <input type="password" name="password2" id="password2" />
                    <div className="helptext">Enter the same password as before, for verification.</div>
                </div>

                <button type="submit">Sign Up</button>
            </form>
        );
    }
});

var SuccessWidget = React.createClass({
    propTypes: {
        username: React.PropTypes.string.isRequired,
        email: React.PropTypes.string.isRequired,
    },
    render: function() {
        return (
            <div>
                <p>Account created! You submitted the following fields:</p>
                <ul>
                    <li>User Name: {this.props.username}</li>
                    <li>Email: {this.props.email}</li>
                </ul>
            </div>
        );
    }
});


var SignupPage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: ""});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            username = $("input#username").val(),
            email = $("input#email").val(),
            password1 = $("input#password1").val(),
            password2 = $("input#password2").val();

        $.post("/signup",
            {
                username: username,
                email: email,
                password1: password1,
                password2: password2
            },
            function success() {
                _this.setState({
                    success: true,
                    email: email,
                    username: username
                });
            })
            .fail(function (res) {
                _this.setState({
                    success: false,
                    error: res.responseJSON.error
                });
            });
    },
    render: function() {
        return (
            <div>
                <p>{this.state.error}</p>
                {this.state.success ?
                    <SuccessWidget email={this.state.email}
                                   username={this.state.username}/>
                    : null
                }
                {this.state.success ?
                    null
                    : <SignupForm submitHandler={this.handleSubmit}
                                  error={this.state.error} />
                }
            </div>
        );
    }
});

ReactDOM.render(
    <SignupPage />,
    document.getElementById("content")
);
