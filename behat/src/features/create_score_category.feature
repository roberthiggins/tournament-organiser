Feature: Create a score category for a tournament
    In order to set percentages for tournament scores
    As an organiser
    I want to be able to classify scores into groups

    Background: Set up a tournament
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "darkness"
        When I press "Login"
        Then I should be on "/"
        Given I am on "/createtournament"
        When I fill in "id_inputTournamentName" with "category_test"
        When I fill in "id_inputTournamentDate" with "2030-03-15"
        When I press "Create"

#    Scenario Outline: Create a simple score category
#    Scenario: Create two score categories for the same tournament
#    Scenario: Two categories make more than a 100% total score

    Scenario Outline: Score categories - malformed
        When I GET "/getScoreCategories/<id>" from the API
        Then the API response status code should be <code>
        Examples:
            |id                 |code   |
            |foo                |404    |
            |                   |404    |
            |ranking_test       |200    |

    Scenario: I want to see all the categories for a tournament
        When I GET "/getScoreCategories/ranking_test" from the API
        Then the response is JSON
        Then the API response should contain "Battle"
        Then the API response should contain "Fair Play"

    Scenario Outline: I try and create a score category through the API
        When I POST "<value>" to "/setScoreCategory" from the API
        Then the API response should contain "<response_text>"
        Then the API response status code should be <code>
        Examples:
            |value                                                              |code|response_text                             |
            |foo                                                                |400 |Enter the required fields                 |
            |category=shiniest_shoes&percentage=5                               |400 |Enter the required fields                 |
            |tournament=category_test&percentage=5                              |400 |Enter the required fields                 |
            |tournament=category_test&category=shiniest_shoes                   |400 |Enter the required fields                 |
            |tournament=category_test&category=shiniest_shoes&percentage=       |400 |Enter the required fields                 |
            |tournament=category_test&category=&percentage=5                    |400 |Enter the required fields                 |
            |tournament=foo&category=shiniest_shoes&percentage=5                |400 |Tournament foo not found in database      |
            |tournament=category_test&category=shiniest_shoes&percentage=a      |400 |percentage must be an integer             |
            |tournament=category_test&category=shiniest_shoes&percentage=15     |200 |Score category set: shiniest_shoes        |
            |tournament=category_test&category=over_the_top&percentage=90       |400 |percentage too high: over_the_top         |
            |tournament=category_test&category=best_set&percentage=45           |200 |Score category set: best_set              |
