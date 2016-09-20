var React = require('react'),
    ReactDOM = require('react-dom');

var UserTaskList = React.createClass({
    render: function() {
        return (
            <div>

                <h2>Welcome to the Tournament Organiser</h2>
                <p>Here you can play in or organise wargaming tournaments. Log in to see lists of tournaments you can enter or create your own.</p>

                <p>
                    <strong>
                        This site is currently under construction. It is in an alpha state only.
                    </strong>
                </p>
                <p>
                    <strong>Check out the Masters Rankings over at <a href="http://rankings.thefieldsofblood.com/region=1&amp;game=5">Fields of Blood</a>
                    </strong>
                </p>
                <ul>
                    <li><a href="signup">Sign Up</a></li>
                    <li><a href="login">Login</a></li>
                    <li><a href="tournaments">See a list of tournaments</a></li>
                    <li><a href="suggestimprovement">Suggest Improvement</a></li>
                </ul>    
           </div>
        );
    }
});

ReactDOM.render(
    <UserTaskList />,
    document.getElementById('content')
);
