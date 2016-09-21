Feature: Place feedback to improve the sight
    In order to improve my experience onthe site
    As a site visitor
    I want to be able to log feedback

    Background:
        Given I am authenticated as "charlie_murphy" using "password"

    @javascript
    Scenario: I navigate to the feedback section
        Given I am on "/devindex"
        Then I should see "Place Feedback" appear
        When I follow "Place Feedback"
        Then I should see "Please give us feedback on your experience on the site" appear
        Given I am on "/feedback"
        Then I should see "Please give us feedback on your experience on the site" appear

    @javascript
    Scenario Outline: I enter some information
        Given I am on "/feedback"
        Then I should see "Please give us feedback" appear
        When I fill in "feedback" with "<content>"
        When I press "Submit"
        Then I should see "<response>" appear

        Examples:
            |content         |response                               |
            |                |Please fill in the required fields     |
            |lkjsdflkjsdflkj |Thanks for you help improving the site |
