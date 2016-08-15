Feature: Register for a Tournament
    In order to play competitive games
    As an account holder
    I need to be able to sign up to a tournament

    Background:
        Given I am authenticated as "charlie_murphy" using "password"

    @javascript
    Scenario: I visit the register page from the front page
        Given I am on "/devindex"
        When I wait for "Register To Play In ranking_test" to appear
        When I follow "Register To Play In ranking_test"
        Then I should see "Apply to play in ranking_test" appear

    @javascript
    Scenario: I visit the register page via the URL
        Given I am on "/tournament/ranking_test"
        Then I should see "Apply to play in ranking_test" appear

    @javascript
    Scenario Outline: I try to apply
        Given I am on "/tournament/<tournament>"
        When I wait for "Apply to play in <tournament>" to appear
        When I press "Apply to play in <tournament>"
        Then I should see "<response>" appear

        Examples:
            | tournament    | response                      |
            | conquest_2095 | Application submitted         |
            | southcon_2095 | Application submitted         |
            | conquest_2095 | You've already applied to conquest_2095    |
            | northcon_2095 | northcon_2095 clashes with southcon_2095   |
