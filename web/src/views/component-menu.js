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
                <a className="menu_link" href={this.props.userAction.href}>
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

        return (<div>
            <div className="menu_title">{this.props.title}</div>
            <ul>
                {listItems}
            </ul>
        </div>);
    }
});

var UserActionList = React.createClass({
    getInitialState: function() {
        return {lists: []};
    },
    componentDidMount: function() {
        this.serverRequest = $.get("/menu/content",
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
        return (<div>{namedLists}</div>);
    }
});

ReactDOM.render(
    <UserActionList />,
    document.getElementById("menu")
);
