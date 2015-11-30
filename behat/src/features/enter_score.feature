Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    # There are two ways to enter the score, using tournament id and player id
    # or by using the entry id directly

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
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=1000                   |400            |Invalid score: 1000                    |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=-3                     |400            |Invalid score: -3                      |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=14                     |200            |Score entered for rick_james: 14       |
            |username=rick_james&tournament=painting_test&key=fanciest_wig&value=12                     |400            |12 not entered. Score is already set   |
            |username=rick_james&username=rick_james&tournament=painting_test&key=fanciest_wig&value=9  |400            |9 not entered. Score is already set    |
            |username=rick_james&username=jerry&tournament=painting_test&key=fanciest_wig&value=8       |400            |8 not entered. Score is already set    |


    # TODO User controls
    Scenario: another player
    Scenario: to
