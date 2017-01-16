/* global $ React ReactDOM:true */

var Inputs = require("./component-inputs.js");

var UpdateDetails = React.createClass({
    propTypes: {
        changeHandler: React.PropTypes.func.isRequired,
        user: React.PropTypes.object.isRequired
    },
    render: function() {
        return (
            <div>
                <div className="form_field">
                    <label htmlFor="username">Username: </label>
                    <span>{this.props.user.username}</span>
                    <div className="helptext">This cannot be changed</div>
                </div>

                <Inputs.textField name="Email"
                                  id="email"
                                  changeHandler={this.props.changeHandler}
                                  value={this.props.user.email || ""} />

                <Inputs.textField name="First Name"
                                  id="first_name"
                                  changeHandler={this.props.changeHandler}
                                  value={this.props.user.first_name || ""} />

                <Inputs.textField name="Last Name"
                                  id="last_name"
                                  changeHandler={this.props.changeHandler}
                                  value={this.props.user.last_name || ""} />
            </div>
        );
    }
});

var SuccessWidget = React.createClass({
    propTypes: {
        user: React.PropTypes.object.isRequired
    },
    render: function() {
        return (
            <div>
                <p>Account updated! Here are your details:</p>
                <ul>
                    <li>User Name: {this.props.user.username}</li>
                    <li>Email: {this.props.user.email}</li>
                    <li>First Name: {this.props.user.first_name}</li>
                    <li>Last Name: {this.props.user.last_name}</li>
                </ul>
            </div>
        );
    }
});


var UpdatePage = React.createClass({
    getInitialState: function () {
        return ({error: "", success: false, user: {}});
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
    handleChange: function(event) {
        var newUser = this.state.user;

        newUser[event.target.id] = event.target.value;
        this.setState({user: newUser});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        $.post(window.location,
            this.state.user,
            function success() {
                this.setState({
                    error: null,
                    success: true,
                    });
                }.bind(this))
            .fail(function (res) {
                this.setState({
                    success: false,
                    error: res.responseJSON.error
                    });
                }.bind(this));
    },
    render: function() {
        return (
            <div>
                {this.state.success ?
                    <SuccessWidget user={this.state.user} />
                    : <form onSubmit={this.handleSubmit}>
                        <h2>You can add/change your details here:</h2>

                        <div>{this.state.error}</div>

                        <UpdateDetails changeHandler={this.handleChange}
                                       user={this.state.user} />
                        <button type="submit">Update</button>
                    </form>}
            </div>
        );
    }
});

ReactDOM.render(
    <UpdatePage />,
    document.getElementById("content")
);
