Feature: Place feedback to improve the sight
    In order to improve my experience onthe site
    As a site visitor
    I want to be able to log feedback

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario Outline: I navigate to the feedback section
        Given I am on "/<start_point>"
        When I follow "<link>"
        Then I should see "<intro>"
        Given I am on "/<url>"
        Then I should see "<intro>"

        Examples:
            | start_point       | url                       | link                  | intro                                                         |
            | devindex          | feedback                  | Place Feedback        | Please give us feedback on your experience on the site        |
            | devindex          | suggestimprovement        | Suggest Improvement   | Suggest a feature you would like to see on the site           |
            |                   | suggestimprovement        | Suggest Improvement   | Suggest a feature you would like to see on the site           |

    Scenario Outline: I enter some information
        Given I am on "/<url>"
        When I fill in "inputFeedback" with "<content>"
        When I press "Submit"
        Then I should see "<response>"

        Examples:
            |url                |content         |response                                      |
            |feedback           |                |This field is required                        |
            |feedback           |lkjsdflkjsdflkj |Thanks for you help improving the site        |
            |suggestimprovement |                |This field is required                        |
            |suggestimprovement |lkjsdflkffffffj |Thanks for you help improving the site        |
            |suggestimprovement |lkjsdflkffffffj |Thanks for you help improving the site        |
