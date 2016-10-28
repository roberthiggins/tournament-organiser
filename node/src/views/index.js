/* global React ReactDOM:true */
var UserTaskList = React.createClass({
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
                <span>
                    <a href="signup">Sign Up</a>
                </span>
                <span>
                    <a href="login">Login</a>
                </span>
                <span>
                    <a href="tournaments">See a list of tournaments</a>
                </span>
                <span>
                    <a href="suggestimprovement">Suggest Improvement</a>
                </span>
           </div>
        );
    }
});

ReactDOM.render(
    <UserTaskList />,
    document.getElementById("content")
);
