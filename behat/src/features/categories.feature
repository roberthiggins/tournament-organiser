Feature: Modify the scoreing categories for a tournament
    In orger to run the tournament
    As a TO
    I need to be able to view and set the scoreing categories for a tournament (battle, sports, etc)

    Scenario Outline: I get a list of the tournament categories from the API
        When I GET "/getScoreCategories/<tournament>" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should be a list of length <cats>
        Then the API response should contain "<cat_1>"
        Then the API response should contain "<cat_2>"

        Examples:
            | tournament        | cats  | cat_1         | cat_2         |
            | southcon_2095     | 1     | some_category | some_category |
            | ranking_test      | 2     | Battle        | Fair Play     |
            | category_test     | 1     | category_1    | category_1    |


    Scenario Outline: I get a list of categories from a non-existent tournament
        When I GET "/getScoreCategories/<tournament>" from the API
        Then the API response status code should be <code>
        Then the API response should contain "<response_text>"

        Examples:
            | tournament   | code  | response_text                      |
            | not_a_thing  | 404   | Tournament not_a_thing not found   |
            | southcon_209 | 404   | Tournament southcon_209 not found  |
            |              | 404   | Not Found                          |


    Scenario: I get a list of categories from a tournament with none
        When I GET "/getScoreCategories/mission_test" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should be a list of length 0
