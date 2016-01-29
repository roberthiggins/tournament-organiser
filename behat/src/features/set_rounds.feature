Feature: Set the number of rounds
    I want to see and change the number of rounds in a tournament
    As a TO
    So that the tournament can have more than one round

    Background: Login
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        Then I should be on "/"

    Scenario: I check the number of rounds in a tournament
        Given I am on "/setrounds/northcon_2095"
        Then the response status code should be 200
        Then I should see "5"

    Scenario: I change that number
        Given I am on "/setrounds/ranking_test"
        When I fill in "numRounds" with "8"
        When I press "Set"
        Then the response status code should be 200
        Then I should be on "/setrounds/ranking_test"
        Then I should see "8"
        Then I should not see "5"
        Given I GET "/tournamentDetails/ranking_test" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should contain "8"

    Scenario: I check a newly minted tournament
        Given I am on "/createtournament"
        When I fill in "id_inputTournamentName" with "round_test"
        When I fill in "id_inputTournamentDate" with "2030-03-15"
        When I press "Create"
        Given I am on "/setrounds/round_test"
        Then the "numRounds" field should contain "5"

    Scenario: I set some insane values for the number of rounds
