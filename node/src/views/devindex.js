/* global $ React ReactDOM:true */

var UserTask = React.createClass({
    propTypes: {
        userAction: React.PropTypes.object.isRequired
    },
    render: function() {
        if (typeof this.props.userAction.href === "undefined") {
            return (<li>{this.props.userAction.text}</li>);
        }

        return (
            <li>
                <a href={this.props.userAction.href}>
                    {this.props.userAction.text}
                </a>
            </li>
        );
    }
});

var NamedList = React.createClass({
    propTypes: {
        items: React.PropTypes.array,
        title: React.PropTypes.string.isRequired,
    },
    render: function() {
        var listItems = this.props.items.map(function(userAction, idx) {
                return (
                    <UserTask userAction={userAction} key={idx} />
                );
            });

        return (
            <div className="userAction">
                <h2 className="actionGroup">
                    {this.props.title}
                </h2>
                <ul>
                    {listItems}
                </ul>
            </div>
        );
    }
});

var UserTaskList = React.createClass({
    getInitialState: function() {
        return {lists: []};
    },
    componentDidMount: function() {
        this.serverRequest = $.get(window.location + "/content",
            function (result) {
                this.setState({lists: result});
            }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        var namedLists = this.state.lists.map(function(namedList, idx) {
            return (
                <NamedList title={namedList.title} items={namedList.actions}
                           key={idx} />
            );
        });

        return (
            <div className="userTaskList">
                <h2>
                    Basic behaviour for players as per documentation in the roles section.
                </h2>
                {namedLists}
           </div>
        );
    }
});

ReactDOM.render(
    <UserTaskList />,
    document.getElementById("content")
);
