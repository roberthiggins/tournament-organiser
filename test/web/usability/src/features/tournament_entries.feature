Feature: List Entries for a tournament
    I want to see all the people who have entered a tournament
    As a prospective player
    As this might influence my decision as to whether to enter

    @javascript
    Scenario Outline: I see some messages
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/<tourn>/entries"
        Then I should see "<message>" appear

        Examples:
            | tourn        | message                                      |
            | entries_test | entries_test_p_1                             |
            | not_a_thing  | Tournament not_a_thing not found in database |

    @javascript
    Scenario: I enter the tournament from the page
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/empty_tournament/entries"
        Then I should see "There are no entries yet. Be the first!" appear
        Then I follow "Be the first!"
        Then I am on "/tournament/empty_tournament/register"
