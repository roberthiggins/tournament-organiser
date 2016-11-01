Feature: DEMO TOURNAMENT
    To see a tournament in action
    As a developer
    I want to simulate an entire tournament

    @javascript
    Scenario Outline: Create TO and players

        # Create a TO and some players
        Given I am on "/signup"
        When I wait for "Username" to appear
        When I wait for "Username" to appear
        When I fill in "username" with "<username>"
        When I fill in "email" with "<username>@demo.com"
        When I fill in "password1" with "<username>_password"
        When I fill in "password2" with "<username>_password"
        When I press "Sign Up"
        Then I should see "Account created" appear

        Examples:
            | username |
            | demo_to  |
            | demo_p1  |
            | demo_p2  |
            | demo_p3  |
            | demo_p4  |
            | demo_p5  |
            | demo_p6  |

    @javascript
    Scenario: TO sets up
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I visit the tournament creation page
        When I fill in "name" with "demo"
        When I fill in "date" with "2056-07-07"
        When I fill in "rounds" with "6"
        When I press "Create"
        Then I should see "Tournament created" appear

        Given I am on "/tournament/demo/missions"
        Then I wait for "Set the missions for demo here" to appear
        When I fill in "missions_0" with "mission_01"
        When I fill in "missions_1" with "mission_02"
        When I fill in "missions_2" with "mission_03"
        When I fill in "missions_3" with "mission_04"
        When I fill in "missions_4" with "mission_05"
        When I fill in "missions_5" with "mission_06"
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
            | demo_p5  |
            | demo_p6  |

    @javascript
    Scenario: TO does the draw for round 1
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/1/draw"
        Then I should see "mission_01" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p1  | 15    |
            | demo_p2  | 15    |
            | demo_p3  | 15    |
            | demo_p4  | 5     |
            | demo_p5  | 5     |
            | demo_p6  | 5     |

    @javascript
    Scenario: TO does the draw for round 2
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/2/draw"
        Then I should see "mission_02" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 2
        # P6 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p6  | 15    |
            | demo_p1  | 15    |
            | demo_p2  | 15    |
            | demo_p3  | 5     |
            | demo_p4  | 5     |
            | demo_p5  | 5     |

    @javascript
    Scenario: TO does the draw for round 3
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/3/draw"
        Then I should see "mission_03" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 3
        # P6 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p5  | 15    |
            | demo_p6  | 15    |
            | demo_p1  | 15    |
            | demo_p2  | 5     |
            | demo_p3  | 5     |
            | demo_p4  | 5     |

    @javascript
    Scenario: TO does the draw for round 4
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/4/draw"
        Then I should see "mission_04" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 4
        # P6 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p4  | 15    |
            | demo_p5  | 15    |
            | demo_p6  | 15    |
            | demo_p1  | 5     |
            | demo_p2  | 5     |
            | demo_p3  | 5     |

    @javascript
    Scenario: TO does the draw for round 5
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/5/draw"
        Then I should see "mission_05" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 5
        # P6 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p3  | 15    |
            | demo_p4  | 15    |
            | demo_p5  | 15    |
            | demo_p6  | 5     |
            | demo_p1  | 5     |
            | demo_p2  | 5     |

    @javascript
    Scenario: TO does the draw for round 6
        Given I am authenticated as "demo_to" using "demo_to_password"
        Given I am on "/tournament/demo/round/6/draw"
        Then I should see "mission_06" appear

    @javascript
    Scenario Outline: Players play and enter scores for round 6
        # P6 moved to pos 1
        Given I am authenticated as "<username>" using "<username>_password"
        Given I am on "/tournament/demo/entry/<username>/entergamescore"
        When I wait for "Battle" to appear
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "Score entered for <username>: <score>" appear
        Examples:
            | username | score |
            | demo_p2  | 11    |
            | demo_p3  | 12    |
            | demo_p4  | 13    |
            | demo_p5  | 7     |
            | demo_p6  | 8     |
            | demo_p1  | 9     |

    # Final scores p1 - 64, p6 - 63, p5 - 62, p4 - 58, p3 - 57, p2 - 56

    @javascript
    Scenario: See Rankings
        Given I am on "/tournament/demo/rankings"
        Then I should see "Placings for demo:" appear
        Then I should see "53.33" appear
        Then I should see "52.5" appear
        Then I should see "51.67" appear
        Then I should see "48.33" appear
        Then I should see "47.5" appear
        Then I should see "46.67" appear
