Feature: Modify the scoring categories for a tournament
    In orger to run the tournament
    As a TO
    I need to be able to view and set the scoreing categories for a tournament (battle, sports, etc)

    Background: I set the categories for category_test
        When I POST "tournamentId=category_test&categories=[%22categories_0%22,%22categories_1%22]&categories_0=[%22foo%22,%2210%22,false,%2210%22,%2210%22]&categories_1=[%22bar%22,%2210%22,false,%2210%22,%2210%22]" to "/setScoreCategories" from the API
        Then the API response status code should be 200
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

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
            | category_test     | 2     | foo           | bar           |


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
        When I GET "/getScoreCategories/conquest_2095" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should be a list of length 0

    Scenario: I modify the tournament categories through the API
        When I POST "tournamentId=category_test&categories=[%22categories_0%22]&categories_0=[%22fantasticgibberish%22,%2221%22,true,%2210%22,%2210%22]" to "/setScoreCategories" from the API
        Then the API response status code should be 200
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response status code should be 200
        Then the API response should be a list of length 1
        Then the API response should contain "fantasticgibberish"
        Then the API response should not contain "category_1"

    Scenario Outline: I try to modify the tournament categories through the API incorrectly
        When I POST "<post>" to "/setScoreCategories" from the API
        Then the API response status code should be 400
        Then I GET "/getScoreCategories/southcon_2095" from the API
        Then the API response status code should be 200
        Then the API response should be a list of length 1
        Then the API response should not contain "<category>"

        Examples:
            | category  | post                                                                                           |
            | fooey     | categories=[%22categories_0%22]&categories_0=[%22fooey%22,%2221%22,true,%2210%22,%2210%22]     |
            | fooey     | tournamentId=category_test&categories=[%22categories_0%22]&categories_0=[%22fooey%22,%2221%22,true,%2210%22]     |
            | fooey     | tournamentId=category_test&categories_0=[%22fooey%22,%2221%22,true,%2210%22,%2210%22]          |
            | fooey     | tournamentId=category_test&categories=[%22categories_0%22]&categories_0=[%22fooey%22]          |
            | fooey     | tournamentId=category_test&categories=[%22categories_0%22]&categories_0=[%2221%22]             |
            | fooey     | tournamentId=category_test&categories=[%22categories_1%22]&categories_0=[%22fooey%22,%2221%22] |
            | fooey     | tournamentId=category_test&categories=[%22categories_0%22,%22categories_1%22]&categories_0=[%22fooey%22,%2221%22]&categories_0=[%22barey%22,%2221%22] |

    Scenario: I modify the tournament categories through the webserver
        # Set
        Given I am on "/setcategories/category_test"
        Then the "id_categories_0_0" field should contain "foo"
        Then I fill in "id_categories_0_1" with "70"
        Then I fill in "id_categories_1_0" with "another_category"
        Then I fill in "id_categories_1_1" with "20"
        Then I press "Set"
        Then the response status code should be 200
        Then I should not see "too high"
        Then I should not see "violates"
        # Confirm
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response should be a list of length 2
        Then the API response should contain "foo"
        Then the API response should contain "another_category"
        # Re-submit
        Then I am on "/setcategories/category_test"
        Then I press "Set"
        Then the response status code should be 200
        Then I should not see "too high"
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response should be a list of length 2
        Then the API response should contain "foo"
        Then the API response should contain "another_category"

    Scenario: I replace a category with another
        Given I am on "/setcategories/category_test"
        Then the "id_categories_0_0" field should contain "foo"
        Then I fill in "id_categories_0_0" with "something_something_darkside"
        Then I fill in "id_categories_0_1" with "1"
        Then I press "Set"
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response should be a list of length 2
        Then the API response should contain "something_something_darkside"
        Then the API response should contain "1"
        Then the API response should not contain "another_category"
        Then the API response should not contain "20"

    Scenario Outline: I replace a category with an illegal category
        Given I am on "/setcategories/category_test"
        Then the "id_categories_0_0" field should contain "bar"
        Then I fill in "id_categories_0_0" with "<cat>"
        Then I fill in "id_categories_0_1" with "<val>"
        Then I fill in "id_categories_0_3" with "1"
        Then I fill in "id_categories_0_4" with "1"
        Then I fill in "id_categories_1_0" with ""
        Then I fill in "id_categories_1_1" with ""
        Then I fill in "id_categories_1_3" with "1"
        Then I fill in "id_categories_1_4" with "1"
        Then I press "Set"
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response status code should be 200
        Then the API response should be a list of length 2
        Then the API response should contain "foo"
        Then the API response should contain "10"
        Then the API response should contain "bar"
        Then the API response should contain "10"
        Then the API response should not contain "<cat>"
        Then the API response should not contain "<val>"
        Examples:
            | cat       | val   |
            | oneohone  | 101   |
            | negone    | -1    |
            | letter    | z     |
            | zero      | 0     |
            | null      | null  |
            | none      | None  |


    Scenario: I try to add the same category multiple times
        Given I am on "/setcategories/category_test"
        Then I fill in "id_categories_0_0" with "foo"
        Then I fill in "id_categories_0_1" with "1"
        Then I fill in "id_categories_0_3" with "1"
        Then I fill in "id_categories_0_4" with "1"
        Then I fill in "id_categories_1_0" with "foo"
        Then I fill in "id_categories_1_1" with "1"
        Then I fill in "id_categories_1_3" with "1"
        Then I fill in "id_categories_1_4" with "1"
        Then I press "Set"
        Then I should see "multiple"


    Scenario: I add two illegal categories
        Given I am on "/setcategories/category_test"
        Then the "id_categories_0_0" field should contain "bar"
        Then I fill in "id_categories_0_0" with "oneohone"
        Then I fill in "id_categories_0_1" with "101"
        Then I fill in "id_categories_0_3" with "1"
        Then I fill in "id_categories_0_4" with "1"
        Then I fill in "id_categories_1_0" with "negativeone"
        Then I fill in "id_categories_1_1" with "-1"
        Then I fill in "id_categories_1_3" with "1"
        Then I fill in "id_categories_1_4" with "1"
        Then I press "Set"
        Then I GET "/getScoreCategories/category_test" from the API
        Then the API response should be a list of length 2
        Then the API response should contain "foo"
        Then the API response should contain "10"
        Then the API response should contain "bar"
        Then the API response should contain "10"
        Then the API response should not contain "oneohone"
        Then the API response should not contain "101"
        Then the API response should not contain "negativeone"
        Then the API response should not contain "-1"


    Scenario Outline: I fill in the min and max values
        Given I am on "/setcategories/category_test"
        Then I fill in "id_categories_0_0" with "<cat>"
        Then I fill in "id_categories_0_1" with "10"
        Then I fill in "id_categories_0_3" with "<min>"
        Then I fill in "id_categories_0_4" with "<max>"
        Then I fill in "id_categories_1_0" with ""
        Then I fill in "id_categories_1_1" with ""
        Then I fill in "id_categories_1_3" with ""
        Then I fill in "id_categories_1_4" with ""
        Then I press "Set"
        Then the response status code should be 200
        Then I should see "<message>"

        Examples:
            | cat | min | max | message                                |
            | cat | 3   | 2   | Min Score must be less than Max Score  |
            | cat | a   | b   | Min and Max Scores must be integers    |
            | cat | 3   | c   | Min and Max Scores must be integers    |
            | cat | d   | 2   | Min and Max Scores must be integers    |
            | cat |     | 2   | Min and Max Scores must be integers    |
            | cat | 3   |     | Min and Max Scores must be integers    |
            | cat |     |     | Min and Max Scores must be integers    |
            | cat | -1  | 2   | Min Score cannot be negative           |
            | cat | 3   | -1  | Max Score must be positive             |
            | cat | 0   | 0   | Max Score must be positive             |
            |     | 1   | 1   | Category must have a name              |
            | cat | 1   | 1   | Score categories set                   |
            | cat | 1   | 2   | Score categories set                   |
