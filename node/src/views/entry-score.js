var React = require("react"),
    ReactDOM = require("react-dom"),
    $ = require("jquery");

var EnterScoreForm = React.createClass({
    propTypes: {
        categories: React.PropTypes.array.isRequired,
        submitHandler: React.PropTypes.func.isRequired
    },
    render: function() {
        return (
            <form onSubmit={this.props.submitHandler}>
                <p>
                    <label htmlFor="value">Score:</label>
                    <input type="text" name="value" id="value" />
                </p>
                <p>
                    <label htmlFor="key">Select a score category:</label>
                    <select name="key" id="key">
                        {this.props.categories}
                    </select>
                </p>
                <button type="submit">Enter Score</button>
            </form>
        );
    }
});

var EnterScorePage = React.createClass({
    getInitialState: function () {
        return ({error: "", successText: "", categoryOptions: [] });
    },
    componentDidMount: function() {

        var perTournCats = function(categories) {
            if (!categories) {
                return [];
            }

            return categories
                .filter(function(cat) {
                    return cat.per_tournament;
                })
                .map(function(cat, idx){
                    return (
                        <option value={cat.name} key={idx}>
                            {cat.name}
                        </option>);
                });
        };


        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                if (result.error) {
                    this.setState({successText : result.error});
                    return;
                }

                result.categoryOptions = perTournCats(result.categories);

                this.setState(result.categoryOptions.length < 1 ?
                    {
                        error: "",
                        message: "",
                        successText: "No per-tournament categories available"
                    }
                    : result);
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    handleSubmit: function (e) {
        e.preventDefault();
        var _this = this;

        $.post(window.location,
            $("form").serialize(),
            function success(res) {
                _this.setState(
                    {successText: res.message, error: "", message: ""});
            })
            .fail(function (res) {
                _this.setState(res.responseJSON);
            });
    },
    render: function() {
        return (
            <div>
                <div>{this.state.successText}</div>
                <div>{this.state.error}</div>
                <div>{this.state.message}</div>
                {
                    this.state.successText ?
                        null
                        : <EnterScoreForm submitHandler={this.handleSubmit}
                                categories={this.state.categoryOptions} />
                }
            </div>
        );
    }
});


ReactDOM.render(
    <EnterScorePage />,
    document.getElementById("content")
);
