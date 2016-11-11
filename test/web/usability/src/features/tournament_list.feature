Feature: See upcoming tournaments
    I want to see a list of available tournaments
    As a user
    So that I can apply for them and check for clashes

    @javascript
    Scenario: I visit the page
        Given I am authenticated as "superman" using "password"
        Given I am on "/"
        When I wait for "See upcoming tournaments" to appear
        When I follow "See upcoming tournaments"
        Then I should be on "/tournaments"
        Then I should see "Upcoming Tournaments" appear
        Then I should see "northcon_2095" appear
        Then I should see "Date: 2095-06-01" appear
        Then I should see "Entries: 0" appear

    @javascript
    Scenario: I visit the page via the URL
        Given I am on "/tournaments"
        Then I should be on "/tournaments"
        Then I should see "Upcoming Tournaments" appear
        Then I should see "northcon_2095" appear
        Then I should see "Date: 2095-06-01" appear
        Then I should see "Entries: 0" appear
