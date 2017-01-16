Feature: DEMO TOURNAMENT
    To see a tournament in action
    As a developer
    I want to simulate an entire tournament

    @javascript
    Scenario Outline: Create TO and players

        # Create a TO and some players
        Given I sign up "<username>"

        Examples:
            | username |
            | demo_to  |
            | demo_p1  |
            | demo_p2  |
            | demo_p3  |
            | demo_p4  |

    @javascript
    Scenario: TO sets up
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I visit the tournament creation page
        When I fill in "name" with "demo"
        When I fill in "date" with "2056-07-07"
        When I fill in "rounds" with "3"
        When I press "Create"
        Then I should see "Tournament created" appear

        Given I am on "/tournament/demo/missions"
        Then I wait for "Set the missions for demo here" to appear
        When I fill in "missions_0" with "mission_01"
        When I fill in "missions_1" with "mission_02"
        When I fill in "missions_2" with "mission_03"
        When I press "Set"   
        Then I should see "Tournament demo updated" appear

        Given I visit category page for "demo"
        Given I fill category 0 with "Battle" "100" "1" "20"
        Then I press "Set"
        Then I should see "Tournament demo updated" appear

    @javascript
    Scenario Outline: Players enter
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo"
        When I wait for "Apply to play in demo" to appear
        When I press "Apply to play in demo"
        Then I should see "Application submitted" appear

        Examples:
            | username |
            | demo_p1  |
            | demo_p2  |
            | demo_p3  |
            | demo_p4  |

    @javascript
    Scenario: TO does the draw for round 1
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/1/draw"
        Then I should see "mission_01" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I enter game score "<score>" for entry "<username>" in tournament "demo"
        Examples:
            | username | score |
            | demo_p1  | 15    |
            | demo_p2  | 15    |
            | demo_p3  | 5     |
            | demo_p4  | 5     |

    @javascript
    Scenario: TO does the draw for round 2
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/2/draw"
        Then I should see "mission_02" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 2
        # P4 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I enter game score "<score>" for entry "<username>" in tournament "demo"
        Examples:
            | username | score |
            | demo_p4  | 15    |
            | demo_p1  | 15    |
            | demo_p2  | 5     |
            | demo_p3  | 5     |

    @javascript
    Scenario: TO does the draw for round 3
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/3/draw"
        Then I should see "mission_03" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 3
        # P4 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I enter game score "<score>" for entry "<username>" in tournament "demo"
        Examples:
            | username | score |
            | demo_p3  | 11    |
            | demo_p4  | 12    |
            | demo_p1  | 8     |
            | demo_p2  | 9     |

    # Final scores p2 - 39, p1 - 38, p4 - 32, p3 - 21

    @javascript
    Scenario: See Rankings
        Given I am on "/tournament/demo/rankings"
        Then I should see "Placings for demo:" appear
        Then I should see "63.33" appear
        Then I should see "53.33" appear
        Then I should see "48.33" appear
        Then I should see "35.00" appear
