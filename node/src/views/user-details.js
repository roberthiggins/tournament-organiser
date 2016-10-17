var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var DetailsWidget = React.createClass({
    propTypes: {
        user: React.PropTypes.object.isRequired
    },
    render: function() {
        var user = this.props.user;

        return (
            <div>
                <p>User details for {user.username}:</p>
                <ul>
                    <li>Username: {user.username}</li>
                    <li>Email: {user.email}</li>
                    <li>First Name: {user.first_name}</li>
                    <li>Last Name: {user.last_name}</li>
                </ul>
            </div>
        );
    }

});

var UserDetailsPage = React.createClass({
    getInitialState: function () {
        return ({error: null, message: null, user: null});
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState(result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        return (
            <div>
                {this.state.error ? <div>{this.state.error}</div> : null}
                {this.state.message ? <div>{this.state.message}</div> : null}
                {this.state.user ?
                    <DetailsWidget user={this.state.user} /> : null}
            </div>
        );
    }
});



ReactDOM.render(
    <UserDetailsPage />,
    document.getElementById("content")
);
