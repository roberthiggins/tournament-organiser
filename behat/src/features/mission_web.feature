Feature: Set the missions through the web front end.
    I want to view and change the missions for a tournament through the web
    As a TO
    So I don't have to discuss the missions in person

    Background: I log in
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        Then I should be on "/"

    Scenario: I view the missions for a tournament
        Given I POST "tournamentId=mission_test&missions=[%22missionzz%22,%22boo%22,%22random%22]" to "/setMissions" from the API
        Given I am on "/setmissions/mission_test"
        Then the "id_missions_0" field should contain "missionzz"
        Then the "id_missions_1" field should contain "boo"
        Then the "id_missions_2" field should contain "random"

    Scenario: I set some missions for the tournament
        Given I am on "/setmissions/mission_test"
        When I fill in "missions_0" with "foo"
        When I fill in "missions_1" with "foo"
        When I fill in "missions_2" with "baz"
        When I press "Set"
        Then the response status code should be 200
        Then I should see "[\"foo\", \"foo\", \"baz\"]"

