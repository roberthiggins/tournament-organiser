Feature: Get information about a tournament
    I want to get info about a tournament
    As a prospective player
    So that I can apply to the enter

    Scenario: I check the API for information on northcon_2095
        Given I GET "/tournamentDetails/northcon_2095" from the API
        Then the response is JSON
        Then the response has a "name" property

    Scenario: I check the API for information on not_a_tournament
        When I GET "/tournamentDetails/not_a_tournament" from the API
        Then the API response status code should be 400

