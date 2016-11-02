/* global $ React ReactDOM:true */
var LoginWidget = React.createClass({
    getInitialState: function () {
        return ({error: ""});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            username = $("input#username").val(),
            password = $("input#password").val(),
            getNext = function () {
                // URL manip. You had one job! And now I have to use 'new'.
                return decodeURIComponent((new RegExp('[?|&]' + "next" + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
            };

        $.post("/login", {
            username: username,
            password: password
            },
            function success() {
                window.location.replace(getNext() || "/");
                return false;
            })
            .fail(function (res) {
                _this.setState({error: res.responseJSON.message});
            });
    },
    render: function() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <h2>Login to your account</h2>

                    <div>{this.state.error}</div>
                    <div>
                        <label htmlFor="username">Username:</label>
                        <input type="text" name="username" id="username" />
                    </div>

                    <div>
                        <label htmlFor="password">Password:</label>
                        <input type="password" name="password" id="password" />
                    </div>
                    <button type="submit">Login</button>
                </form>
                <span>
                    <a href="/resetpassword">Forgot Password</a>
                </span>
                <span>
                    <a href="/signup">Create Account</a>
                </span>
            </div>
        );
    }
});

ReactDOM.render(
    <LoginWidget />,
    document.getElementById("content")
);
