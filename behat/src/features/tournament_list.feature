Feature: See a list of tournaments
    I want to see a list of available tournaments
    As a user
    So that I can apply for them and check for clashes

    Scenario: I visit the page
        Given I am on "/"
        When I follow "See a list of tournaments"
        Then I should be on "/tournaments"
        Then I should see "See available tournaments below"
        Then I should see "northcon_2095 - 2095-06-01"

        Given I am on "/devindex"
        When I follow "See a list of tournaments"
        Then I should be on "/tournaments"
        Then I should see "See available tournaments below"
        Then I should see "northcon_2095 - 2095-06-01"

    Scenario: I visit the page via the URL
        Given I am on "/tournaments"
        Then I should be on "/tournaments"
        Then I should see "See available tournaments below"
        Then I should see "northcon_2095 - 2095-06-01"
