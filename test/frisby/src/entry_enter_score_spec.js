describe('Get the next game for an entry', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR'] +
        'tournament/enter_tournament_score_test/entry/';

    frisby.create('No auth enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: '',
                key: 'enter_tournament_score_test_category_1',
                value: 5
            },
            {json: true}
        )
        .expectStatus(403)
        .expectBodyContains('Permission denied')
        .toss()

    frisby.create('No auth enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                key: 'enter_tournament_score_test_category_1',
                value: 5
            },
            {json: true}
        )
        .expectStatus(400)
        .expectBodyContains('Enter the required fields')
        .toss()

    frisby.create('Non-playing user enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'charlie_murphy',
                key: 'enter_tournament_score_test_category_1',
                value: 5
            },
            {json: true}
        )
        .expectStatus(403)
        .expectBodyContains('Permission denied')
        .toss()

    frisby.create('Different entry enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_2',
                key: 'enter_tournament_score_test_category_1',
                value: 5
            },
            {json: true}
        )
        .expectStatus(403)
        .expectBodyContains('Permission denied')
        .toss()

    frisby.create('superuser enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'superuser',
                key: 'enter_tournament_score_test_category_su',
                value: 5
            },
            {json: true}
        )
        .expectStatus(200)
        .expectBodyContains(
            'Score entered for enter_tournament_score_test_p_1: 5')
        .toss()


    frisby.create('to enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'to',
                key: 'enter_tournament_score_test_category_to',
                value: 5
            },
            {json: true}
        )
        .expectStatus(200)
        .expectBodyContains(
            'Score entered for enter_tournament_score_test_p_1: 5')
        .toss()

    frisby.create('player enters a score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_1',
                key: 'enter_tournament_score_test_category_1',
                value: 5
            },
            {json: true}
        )
        .expectStatus(200)
        .expectBodyContains(
            'Score entered for enter_tournament_score_test_p_1: 5')
        .toss()


    frisby.create('player enters a score twice: first score')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_1',
                key: 'enter_tournament_score_test_category_2',
                value: 5
            },
            {json: true}
        )
        .expectStatus(200)
        .expectBodyContains(
            'Score entered for enter_tournament_score_test_p_1: 5')
        .toss()
    frisby.create('player enters a score twice: again')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_1',
                key: 'enter_tournament_score_test_category_2',
                value: 4
            },
            {json: true}
        )
        .expectStatus(400)
        .expectBodyContains('4 not entered. Score is already set')
        .toss()


    frisby.create('score too low')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_1',
                key: 'enter_tournament_score_test_category_3',
                value: 0
            },
            {json: true}
        )
        .expectStatus(400)
        .expectBodyContains('Invalid score: 0')
        .toss()


    frisby.create('score too high')
        .post(API + 'enter_tournament_score_test_p_1/entertournamentscore',
            {
                scorer: 'enter_tournament_score_test_p_1',
                key: 'enter_tournament_score_test_category_4',
                value: 6
            },
            {json: true}
        )
        .expectStatus(400)
        .expectBodyContains('Invalid score: 6')
        .toss()

});
