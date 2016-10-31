/* global React ReactDOM:true */
var IntroPage = React.createClass({
    render: function() {
        return (
            <div>

                <h2>Welcome to the Tournament Organiser</h2>
                <p>Here you can play in or organise wargaming tournaments. Log in to see lists of tournaments you can enter or create your own.</p>

                <h2>
                    This site is currently under construction. It is in an alpha state only.
                </h2>
                <p>
                    <strong>Check out the Masters Rankings over at <a href="http://rankings.thefieldsofblood.com/region=1&amp;game=5">Fields of Blood</a>
                    </strong>
                </p>
           </div>
        );
    }
});


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
                    <li>
                        <a className="menu_link"
                           href="suggestimprovement">Suggest Improvement</a>
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
    <IntroPage />,
    document.getElementById("content")
);
ReactDOM.render(
    <UserActionList />,
    document.getElementById("menu")
);
