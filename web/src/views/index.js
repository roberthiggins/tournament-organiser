/* global React ReactDOM:true */

var IntroPage = React.createClass({
    render: function() {
        return (
            <div>

                <h2>Welcome to the Tournament Organiser</h2>
                <p>Here you can play in or organise wargaming tournaments. Log in to see lists of tournaments you can enter or create your own.</p>

                <p>
                    This site is currently in a BETA state. Please report any issues to <a href="https://github.com/roberthiggins/tournament-organiser" >the github page</a>.
                </p>
                <p>
                    <strong>Check out the Masters Rankings over at <a href="http://rankings.thefieldsofblood.com/region=1&amp;game=5">Fields of Blood</a>
                    </strong>
                </p>
           </div>
        );
    }
});


ReactDOM.render(
    <IntroPage />,
    document.getElementById("content")
);
