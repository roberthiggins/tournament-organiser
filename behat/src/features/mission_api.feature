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

    Scenario: I want to set the missions for a tournament
    Scenario: I want to set the mission for a single round
