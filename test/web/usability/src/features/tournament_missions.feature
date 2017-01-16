Feature: Set the missions through the web front end.
    I want to view and change the missions for a tournament through the web
    As a TO
    So I don't have to discuss the missions in person

    @javascript
    Scenario: I view the change missions for a tournament
        Given I am authenticated as "mission_test_to" using "password"
        Given I am on "/tournament/mission_test/missions"
        Then I wait for "Set the missions for mission_test here" to appear
        Then the "missions_0" field should contain "Mission the First"
        Then the "missions_1" field should contain "Mission the Second"
        Then the "missions_2" field should contain "Mission the Third"
        When I fill in "missions_1" with "some_mission"
        When I press "Set"
        Then I should see "Tournament mission_test updated" appear
        Given I am on "/tournament/mission_test/missions"
        Then I should see "some_mission" appear in field "missions_1"

    @javascript
    Scenario: I visit a non-existent tournament
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/foo/missions"
        Then I wait for "Tournament foo not found in database" to appear

    @javascript
    Scenario: I visit a tournament with no rounds set
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/empty_tournament/missions"
        Then I wait for "Please set the number of rounds for empty_tournament first" to appear
