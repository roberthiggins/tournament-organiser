Feature: Modify the scoring categories for a tournament
    In orger to run the tournament
    As a TO
    I need to be able to view and set the scoreing categories for a tournament (battle, sports, etc)

    @javascript
    Scenario Outline: I see some messages
        Given I am authenticated as "category_test_to" using "password"
        Given I visit category page for "category_test"
        Given I fill category 0 with "<cat>" "<val>" "1" "1"
        Given I fill category 1 with "" "" "" ""
        Given I fill category 2 with "" "" "" ""
        Then I press "Set"
        Then I should see "<message>" appear

        Examples:
            | cat      | val | message                               |
            | good     | 10  | Tournament category_test updated      |
            | oneohone | 101 | Percentage must be an integer (1-100) |
