Feature: Place feedback to improve the sight
    In order to improve my experience onthe site
    As a site visitor
    I want to be able to log feedback

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: I navigate to the feedback section
        Given I am authenticated as "charlie_murphy" using "password"
        Given I am on "/devindex"
        When I wait for 1 second
        When I follow "Place Feedback"
        Then I should see "Please give us feedback on your experience on the site"
        Given I am on "/feedback"
        Then I should see "Please give us feedback on your experience on the site"

    @javascript
    Scenario Outline: I enter some information
        Given I am authenticated as "charlie_murphy" using "password"
        Given I am on "/feedback"
        When I wait for 1 second
        When I fill in "feedback" with "<content>"
        When I press "Submit"
        When I wait for 1 second
        Then I should see "<response>"

        Examples:
            |content         |response                               |
            |                |Please fill in the required fields     |
            |lkjsdflkjsdflkj |Thanks for you help improving the site |
