/* global $ React ReactDOM:true */
var InputWidget = React.createClass({
    propTypes: {
        submitHandler: React.PropTypes.func,
        error: React.PropTypes.string
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler} >
                <p>Please give us feedback on your experience on the site</p>

                <div>{this.props.error}</div>
                <div>
                    <label htmlFor="feedback">Feedback:</label>
                    <textarea name="feedback"
                              id="feedback"
                              rows="10"
                              cols="40"
                              maxLength="500"/>
                </div>

                <button type="submit">Submit</button>
            </form>
        );
    }
});

var FeedbackWidget = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: ""});
    },
    handleSubmit: function (e) {
        // you are the devil! This controller crap should be in a separate file.
        e.preventDefault();
        var _this = this,
            feedback = $("textarea#feedback").val();

        $.post("/feedback",
            { feedback: feedback },
            function success(res) {
                _this.setState({successText: res.message});
            })
            .fail(function (res) {
                _this.setState({error: res.responseJSON.message});
            });
    },
    render: function() {
        return (
            <div>
                {
                    this.state.successText ?
                        <div>{this.state.successText}</div>
                        : null
                }
                {
                    this.state.successText ?
                        null
                        : <InputWidget submitHandler={this.handleSubmit}
                                     error={this.state.error} />
                }
            </div>
        );
    }
});



ReactDOM.render(
    <FeedbackWidget />,
    document.getElementById("content")
);
