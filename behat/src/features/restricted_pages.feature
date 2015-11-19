Feature: Restricted pages
    I want to be able to restrict the pages that a user can get to
    As a user experience developer
    To ensure users can't get to pages they can't use

    Background:
        Given I am on "/logout"

    Scenario Outline:
        Given I am on "/<direct>"
        Then I should be on "/login?next=/<direct>"
        Given I am on "/"
        When I follow "<link>"
        Then I should be on "/login?next=/<direct>"


        Examples:
            |direct                     |link                           |
            |createtournament           |Create a Tournament            | 
            |feedback                   |Place Feedback                 | 
            |registerforatournament     |Register for a Tournament      | 
            |suggestimprovement         |Suggest Improvement            | 
