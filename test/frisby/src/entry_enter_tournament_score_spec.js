describe('Enter a tournament score for an entry', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR + 'tournament/enter_score_test/entry/';

    frisby.create('No auth enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_1',
                value: 5
            },
            {json: true})
        .expectStatus(401)
        .expectBodyContains('Could not verify your access level')
        .toss();

    frisby.create('Non-playing user enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_1',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('charlie_murphy:password').toString("base64"))
        .expectStatus(403)
        .expectBodyContains('Permission denied')
        .toss();

    frisby.create('Different entry enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_1',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_2:password').toString("base64"))
        .expectStatus(403)
        .expectBodyContains('Permission denied')
        .toss();

    frisby.create('superuser enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_su',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(200)
        .expectBodyContains('Score entered for enter_score_test_p_1: 5')
        .toss();


    frisby.create('to enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_to',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_to:password').toString("base64"))
        .expectStatus(200)
        .expectBodyContains('Score entered for enter_score_test_p_1: 5')
        .toss();

    frisby.create('player enters a score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_1',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(200)
        .expectBodyContains('Score entered for enter_score_test_p_1: 5')
        .toss();


    frisby.create('player enters a score twice: first score')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_2',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(200)
        .expectBodyContains('Score entered for enter_score_test_p_1: 5')
        .toss();
    frisby.create('player enters a score twice: again')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_2',
                value: 4
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(400)
        .expectBodyContains('4 not entered. Score is already set')
        .toss();


    frisby.create('score too low')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_3',
                value: 0
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(400)
        .expectBodyContains('Invalid score: 0')
        .toss();


    frisby.create('score too high')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_3',
                value: 6
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(400)
        .expectBodyContains('Invalid score: 6')
        .toss();

    frisby.create('Non-existent category')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_non_existent',
                value: 6
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(400)
        .expectBodyContains('Unknown category: enter_score_test_category_non_existent')
        .toss();

    frisby.create('Per game category')
        .post(API + 'enter_score_test_p_1/entertournamentscore',
            {
                key: 'enter_score_test_category_per_game_1',
                value: 5
            },
            {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('enter_score_test_p_1:password').toString("base64"))
        .expectStatus(400)
        .expectBodyContains('enter_score_test_category_per_game_1 should be entered per-tournament')
        .toss();

});
