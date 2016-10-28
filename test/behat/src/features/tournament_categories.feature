Feature: Modify the scoring categories for a tournament
    In orger to run the tournament
    As a TO
    I need to be able to view and set the scoreing categories for a tournament (battle, sports, etc)

    Background: I set the categories for category_test
        Given I am authenticated as "category_test_to" using "password"
        Given I visit category page for "category_test"
        Given I fill category 0 with "foo" "10" "10" "10"
        Given I fill category 1 with "bar" "10" "10" "10"
        Then I press "Set"
        Then I should see "Tournament category_test updated" appear
        Given I visit category page for "category_test"

    @javascript
    Scenario: I modify the tournament categories through the webserver
        # Set
        Given I fill category 0 with "foo" "10" "10" "10"
        Given I fill category 1 with "another_cat" "10" "10" "10"
        Then I press "Set"
        Then I should see "Tournament category_test updated" appear
        # Confirm
        Given I visit category page for "category_test"
        Then the "0_name" field should contain "another_cat"
        Then the "1_name" field should contain "foo"
        Then the "2_name" field should contain ""
        # Re-submit
        Then I press "Set"
        Then I should see "Tournament category_test updated" appear
        Given I visit category page for "category_test"
        Then the "0_name" field should contain "another_cat"
        Then the "1_name" field should contain "foo"
        Then the "2_name" field should contain ""

    @javascript
    Scenario: I replace a category with another
        Given I fill category 0 with "baz" "10" "10" "10"
        Then I press "Set"
        Then I should see "Tournament category_test updated" appear
        Given I visit category page for "category_test"
        Then the "0_name" field should contain "baz"
        Then the "1_name" field should contain "foo"
        Then the "2_name" field should contain ""

    @javascript
    Scenario: I remove the categories
        Given I fill category 0 with "" "" "" ""
        Given I fill category 1 with "" "" "" ""
        Then I press "Set"
        Then I should see "Tournament category_test updated" appear
        Given I visit category page for "category_test"
        Then the "0_name" field should contain ""
        Then the "1_name" field should contain ""

    @javascript
    Scenario Outline: I replace a category with an illegal category
        Given I fill category 0 with "<cat>" "<val>" "1" "1"
        Then I press "Set"
        Given I visit category page for "category_test"
        Then the "0_name" field should contain "bar"
        Then the "1_name" field should contain "foo"
        Then the "2_name" field should contain ""

        Examples:
            | cat       | val   |
            | oneohone  | 101   |
            | negone    | -1    |
            | letter    | z     |
            | zero      | 0     |
            | null      | null  |
            | none      | None  |

    @javascript
    Scenario: I try to add the same category multiple times
        Given I fill category 1 with "bar" "10" "10" "10"
        Then I press "Set"
        Then I should see "multiple" appear

    @javascript
    Scenario Outline: I fill in the min and max values
        Given I fill category 0 with "<cat>" "10" "<min>" "<max>"
        Then I press "Set"
        Then I should see "<message>" appear

        Examples:
            | cat | min | max | message                                |
            | cat | 3   | 2   | Min Score must be less than Max Score  |
            | cat | a   | b   | Min and Max Scores must be integers    |
            | cat | 3   | c   | Min and Max Scores must be integers    |
            | cat | d   | 2   | Min and Max Scores must be integers    |
            | cat |     | 2   | Please fill in all fields              |
            | cat | 3   |     | Please fill in all fields              |
            | cat |     |     | Please fill in all fields              |
            | cat | -1  | 2   | Min Score cannot be negative           |
            | cat | 3   | -1  | Max Score must be positive             |
            | cat | 0   | 0   | Max Score must be positive             |
            |     | 1   | 1   | Please fill in all fields              |
            | cat | 1   | 1   | Tournament category_test updated       |
            | cat | 1   | 2   | Tournament category_test updated       |

    @javascript
    Scenario Outline: I fill in some incorrect percentages
        Given I fill category 0 with "cat" "<percentage>" "1" "2"
        Then I press "Set"
        Then I should see "<message>" appear

        Examples:
            | percentage | message                                |
            | -1         | Percentage must be an integer (1-100)  |
            |            | Please fill in all fields              |
            | null       | Percentage must be an integer (1-100)  |
            | None       | Percentage must be an integer (1-100)  |
            | 101        | Percentage must be an integer (1-100)  |
            | 0          | Percentage must be an integer (1-100)  |
