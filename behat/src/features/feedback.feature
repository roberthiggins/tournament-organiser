Feature: Place feedback to improve the sight
    In order to improve my experience onthe site
    As a site visitor
    I want to be able to log feedback

    Scenario Outline: I navigate to the feedback section
        Given I am on "/"
        When I follow "<link>"
        Then I should see "<intro>"
        Given I am on "/<url>"
        Then I should see "<intro>"

        Examples:
            | url                       | link                  | intro                                                         |
            | feedback                  | Place Feedback        | Please give us feedback on your experience on the site        |
            | suggestimprovement        | Suggest Improvement   | Suggest a feature you would like to see on the site           |

    @javascript
    Scenario Outline: I enter some information
        Given I am on "/<url>"
        When I fill in "inputFeedback" with "<content>"
        When I press "Submit"
        When I wait for the response
        Then I should see "<response>"

        Examples:
            |url                |content         |response                                      |
            |feedback           |                |Enter the required fields                     |
            |feedback           |lkjsdflkjsdflkj |Thanks for you help improving the site        |
            |suggestimprovement |                |Enter the required fields                     |
            |suggestimprovement |lkjsdflkffffffj |Thanks for you help improving the site        |
            |suggestimprovement |lkjsdflkffffffj |Thanks for you help improving the site        |
