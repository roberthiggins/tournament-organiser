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
            |tournament=painting_test&key=fanciest_wig&value=20                                         |400            |Enter the required fields              |
            |username=stevemcqueen&key=fanciest_wig&value=20                                            |400            |Enter the required fields              |
            |username=stevemcqueen&username=stevemcqueen&key=fanciest_wig&value=20                      |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&value=20                                    |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&key=fanciest_wig                            |400            |Enter the required fields              |
            |username=stevemcqueen&tournament=painting_test&key=fanciest_wig&                           |400            |Enter the required fields              |
            |username=jimmynoname&tournament=painting_test&key=fanciest_wig&value=20                    |400            |Unknown player: jimmynoname            |
            |username=stevemcqueen&tournament=notatournament&key=fanciest_wig&value=20                  |400            |Unknown tournament: notatournament     |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=ham                    |400            |Invalid score: ham                     |
            |username=rick_james&tournament=painting_test&key=magic&value=20                            |400            |Unknown category: magic                |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=20                     |200            |Score entered for rick_james: 20       |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=19                     |400            |Score already set                      |
            |username=rick_james&username=rick_james&tournament=painting_test&key=fanciest_wig&value=20 |400            |Score already set                      |
            |username=rick_james&username=jerry&tournament=painting_test&key=fanciest_wig&value=20      |400            |Score already set                      |

# Awaiting user controls
#    Scenario: Another player tries to give a painting score to a player
#    Scenario: People try to give best painted votes to a player

