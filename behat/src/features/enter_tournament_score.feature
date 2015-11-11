Feature: Enter a tournament score
    I want to enter once-per-tournament scores
    As tournament organiser or player
    So that I can give people points

    Background:
        # There is a tournamnent that has a  best painted and a per-player
        # painting score. Each player, and the TO, is eligible to give a vote
        # for best painted. Only the TO is eligible to give painting scores to
        # players.

    Scenario Outline: The TO gives a painting score to a player
        When I POST "<value>" to "/entertournamentscore" from the API
        Then the API response should contain "<response_text>"
        Then the API response status code should be <response_code>

        Examples:
            |value                                                                                      |response_code  |response_text                          |
            |foo                                                                                        |400            |Enter the required fields              |
            |tournament=painting_test&key=painting&value=20                                             |400            |Enter the required fields              |
            |username=stevemcqueen&key=painting&value=20                                                |400            |Enter the required fields              |
            |username=stevemcqueen&username=stevemcqueen&key=painting&value=20                          |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&value=20                                    |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&key=painting                                |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&key=painting&                               |400            |Enter the required fields              |
            |username=jimmynoname&tournament=painting_test&key=painting&value=20                        |400            |Unknown user: jimmynoname              |
            |username=stevemcqueen&tournament=notatournament&key=painting&value=20                      |400            |Unknown tournament: notatournament     |
# Awaiting db implementation
#            |username=stevemcqueen&tournament=painting_test&key=painting&value=ham                      |400            |Invalid score: ham                     |
#            |username=stevemcqueen&tournament=notatournament&key=magic&value=20                         |400            |Unknown category: magic                |
#            |username=stevemcqueen&tournament=painting_test&key=painting&value=20                       |200            |Score entered for stevemcqueen: 20     |
#            |username=stevemcqueen&tournament=painting_test&key=painting&value=19                       |200            |Score entered for stevemcqueen: 19     |
#            |username=stevemcqueen&username=stevemcqueen&tournament=painting_test&key=painting&value=20 |200            |Score entered for stevemcqueen: 20     |
#            |username=stevemcqueen&username=jerry&tournament=painting_test&key=painting&value=20        |200            |Score entered for stevemcqueen: 20     |

# Awaiting user controls
#    Scenario: Another player tries to give a painting score to a player
#    Scenario: People try to give best painted votes to a player

