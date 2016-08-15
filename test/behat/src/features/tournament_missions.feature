Feature: Set the missions through the web front end.
    I want to view and change the missions for a tournament through the web
    As a TO
    So I don't have to discuss the missions in person

    Background: I log in
        Given I am authenticated as "charlie_murphy" using "password"
        Given I am on "/tournament/mission_test/missions"
        Then I wait for "Set the missions for mission_test here" to appear
        When I fill in "missions_0" with "missionzz"
        When I fill in "missions_1" with "boo"
        When I fill in "missions_2" with "random"
        When I press "Set"   

    @javascript
    Scenario: I view the missions for a tournament
        Given I am on "/tournament/mission_test/missions"
        Then I wait for "Set the missions for mission_test here" to appear
        Then the "missions_0" field should contain "missionzz"
        Then the "missions_1" field should contain "boo"
        Then the "missions_2" field should contain "random"

    @javascript
    Scenario: I set some missions for the tournament
        Given I am on "/tournament/mission_test/missions"
        When I fill in "missions_0" with "foo"
        When I fill in "missions_1" with "foo"
        When I fill in "missions_2" with "baz"
        When I press "Set"
        Then I should see "Missions set" appear
        Given I am on "/tournament/mission_test/missions"
        Then I wait for "Set the missions for mission_test here" to appear
        Then the "missions_0" field should contain "foo"
        Then the "missions_1" field should contain "foo"
        Then the "missions_2" field should contain "baz"
