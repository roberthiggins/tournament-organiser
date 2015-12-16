Feature: Interact with missions through the API
    I want to be able to get and set missions for a tournament
    As a TO
    So that that players can get mission information without me on the day

    Scenario: I want to get a list of missions for the tournament
        When I GET "/getMissions/mission_test" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should contain "Mission the First"
        Then the API response should contain "Mission the Second"
        Then the API response should contain "Mission the Third"

    Scenario: I want to get the mission for a single round
        # Get the nth element in the list returned getMissions

    Scenario Outline: I want to set the missions for a tournament
        When I POST "<value>" to "/setMissions" from the API
        Then the API response status code should be <code>
        When I GET "/getMissions/mission_test" from the API
        Then the API response should contain "<first_mission>"

        Examples:
            | value                                                                             | code  | first_mission         |
            | tournamentId=mission_test                                                         | 400   | Mission the First     |
            | missions=[%22foo%22,%22bar%22,%22baz%22]                                          | 400   | Mission the First     |
            | tournamentId=mission_test&missions=[%22bar%22,%22baz%22]                          | 400   | Mission the First     |
            | tournamentId=mission_test&missions=[%22bar%22,%22baz%22,%22boo%22,%22boo%22]      | 400   | Mission the First     |
            | tournamentId=mission_test&missions=[%22foo%22,%22bar%22,%22baz%22]                | 200   | foo                   |
            | tournamentId=mission_test&missions=[%22boo%22,%22boo%22,%22boo%22]                | 200   | boo                   |

    Scenario: I want to set the mission for a single round
        #TODO
