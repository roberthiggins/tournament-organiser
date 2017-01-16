/* global $ React ReactDOM:true */
var TournamentInfo = React.createClass({
    propTypes: {
        name: React.PropTypes.string.isRequired,
        entries: React.PropTypes.number,
        date: React.PropTypes.string
    },
    render: function() {
        return (
            <div>
                <ul>
                    <li>Name: {this.props.name}</li>
                    <li>Date: {this.props.date || "N/A"}</li>
                    <li>Confirmed Entries: {this.props.entries || 0}</li>
                </ul>
            </div>
        );
    }
});

var TournamentInfoPage = React.createClass({
    getInitialState: function() {
        return ({successText: "", error: "", user: null});
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
    apply: function(e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this;

        var checkRedirect = function(xhr) {
            if (xhr.responseText && typeof xhr.responseJSON === "undefined") {
                var newDoc = document.open("text/html", "replace");
                newDoc.write(xhr.responseText);
                newDoc.close();
                window.location.replace("/login?next=" + window.location.href);
                return true;
            }
            return false;
        }

        $.post(window.location)
            .done(function (res, status, xhr) {
                if (checkRedirect(xhr)) {
                    return false;
                }
                else {
                    _this.setState({
                        successText: xhr.responseJSON.message,
                        error: ""
                    });
                }
            })
            .fail(function (res) {
                _this.setState(res.responseJSON);
            });
    },
    withdraw: function(e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();

        $.post(window.location + "/entry/" + this.state.user + "/withdraw")
            .done(function (res, status, xhr) {
                this.setState({
                    successText: xhr.responseJSON.message,
                    error: ""
                    });
                }.bind(this))
            .fail(function (res) {
                this.setState(res.responseJSON);
                }.bind(this));
    },
    render: function() {

        var infoWidget = this.state.name && !this.state.successText ?
                 <TournamentInfo name={this.state.name}
                                 entries={this.state.entries}
                                 date={this.state.date} />
                 : null,
            applyWidget = infoWidget && !this.state.user ?
                <form onSubmit={this.apply}>
                    <button type="submit">
                        Apply to play in {this.state.name}
                    </button>
                </form>
                : null,
            withdrawWidget = this.state.user ?
                <form onSubmit={this.withdraw}>
                    <button type="submit">
                        Withdraw from {this.state.name}
                    </button>
                </form>
                : null;

        return (
            <div>
                <h2>Tournament Information</h2>
                <p>{this.state.successText}</p>
                <p>{this.state.error}</p>
                {infoWidget}
                {applyWidget}
                {this.state.user ?
                    <p>You have entered this tournament</p> : null}
                {this.state.user ? withdrawWidget : null}
            </div>
        );
    }
});

ReactDOM.render(
    <TournamentInfoPage />,
    document.getElementById("content")
);
