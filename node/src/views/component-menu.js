/* global React ReactDOM:true */

var UserActionList = React.createClass({
    render: function() {
        return (
            <div>
                <div className="menu_title">Account</div>
                <ul>
                    <li>
                        <a className="menu_link" href="signup">Sign Up</a>
                    </li>
                    <li>
                        <a className="menu_link" href="login">Login</a>
                    </li>
                </ul>
                <div className="menu_title">Play</div>
                <ul>
                    <li>
                        <a className="menu_link"
                           href="tournaments">See a list of tournaments</a>
                    </li>
                </ul>
                <div className="menu_title">Feedback</div>
                <ul>
                    <li>
                        <a className="menu_link"
                           href="suggestimprovement">Suggest Improvement</a>
                    </li>
                </ul>
            </div>);
    }
});

ReactDOM.render(
    <UserActionList />,
    document.getElementById("menu")
);
