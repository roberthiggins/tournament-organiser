describe('Enter score for single game for an entry', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR + 'tournament/enter_score_test/entry/';

    // Some setup
    frisby.create('Set enter_score_test to 1 round')
        .post(
            process.env.API_ADDR + 'tournament/enter_score_test/rounds',
            {numRounds: 1}
        )
        .expectStatus(200)
        .toss();
    frisby.create('get game_id of next game for enter_score_test_p_1')
        .get(API + 'enter_score_test_p_1/nextgame')
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id;

            frisby.create('No auth enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: '',
                        key: 'enter_score_test_category_per_game_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(403)
                .expectBodyContains('Permission denied')
                .toss();

            frisby.create('No auth enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        key: 'enter_score_test_category_per_game_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('Enter the required fields')
                .toss();

            frisby.create('Non-playing user enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'charlie_murphy',
                        key: 'enter_score_test_category_per_game_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(403)
                .expectBodyContains('Permission denied')
                .toss();

            frisby.create('Different entry enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_2',
                        key: 'enter_score_test_category_per_game_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(403)
                .expectBodyContains('Permission denied')
                .toss();

            frisby.create('superuser enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'superuser',
                        key: 'enter_score_test_category_per_game_su',
                        value: 5
                    },
                    {json: true})
                .expectStatus(200)
                .expectBodyContains('Score entered for enter_score_test_p_1: 5')
                .toss();


            frisby.create('to enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'to',
                        key: 'enter_score_test_category_per_game_to',
                        value: 5
                    },
                    {json: true})
                .expectStatus(200)
                .expectBodyContains('Score entered for enter_score_test_p_1: 5')
                .toss();

            frisby.create('player enters a score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_per_game_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(200)
                .expectBodyContains('Score entered for enter_score_test_p_1' +
                    ': 5')
                .toss();


            frisby.create('player enters a score twice: first score')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_per_game_2',
                        value: 5
                    },
                    {json: true})
                .expectStatus(200)
                .expectBodyContains('Score entered for enter_score_test_p_1: 5')
                .toss();
            frisby.create('player enters a score twice: again')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_per_game_2',
                        value: 4
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('4 not entered. Score is already set')
                .toss();


            frisby.create('score too low')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_per_game_3',
                        value: 0
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('Invalid score: 0')
                .toss();


            frisby.create('score too high')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_per_game_3',
                        value: 6
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('Invalid score: 6')
                .toss();

            frisby.create('Non-existent category')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_non_existent',
                        value: 5
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('Unknown category: ' +
                    'enter_score_test_category_non_existent')
                .toss();

            frisby.create('Per tournament category')
                .post(API + 'enter_score_test_p_1/entergamescore',
                    {
                        game_id: gameId,
                        scorer: 'enter_score_test_p_1',
                        key: 'enter_score_test_category_1',
                        value: 5
                    },
                    {json: true})
                .expectStatus(400)
                .expectBodyContains('Cannot enter a per-tournament score ' +
                    '(enter_score_test_category_1) for a game (game_id: ' +
                    gameId + ')')
                .toss();

        })
        .toss();
});
