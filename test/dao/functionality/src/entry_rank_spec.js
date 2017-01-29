describe('Check that players are ranked correctly', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR + 'tournament/';

    frisby.create('Check that the rank_entries format is correct')
        .get(API + 'rank_test/rankings', {inspectOnFailure: true})
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes('0',
            {
                username: String,
                ranking: Number,
                total_score: String,
                entry_id: Number,
                scores: Array,
                tournament_id: String
            })
        .expectJSONTypes('*.0.scores.*',
            {
                category: String,
                max_val: Number,
                score: Number,
                min_val: Number
            })
        .toss();


    frisby.create('Get rankings for a tournament')
        .get(API + 'rank_test/rankings', {inspectOnFailure: true})
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([
            {
                username: 'rank_test_player_1',
                ranking: 1,
                total_score: '84.75',
                scores: [
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 20,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 1,
                        min_val: 1
                    },
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 15,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    }
                ],
                tournament_id: 'rank_test'
            },
            {
                username: 'rank_test_player_4',
                ranking: 2,
                total_score: '66.25',
                scores: [
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 20,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    },
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 5,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    }
                ],
                tournament_id: 'rank_test'
            }])
        .expectJSON('?',
            {
                username: 'rank_test_player_3',
                ranking: 4,
                total_score: '32.50',
                scores: [
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 5,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    }
                ],
                tournament_id: 'rank_test'
            })
        .expectJSON('?',
            {
                username: 'rank_test_player_5',
                ranking: 3,
                total_score: '43.75',
                scores: [
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 0,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    },
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 15,
                        min_val: 0
                    },
               ],
                tournament_id: 'rank_test'
            })
        .expectJSON('?',
            {
                username: 'rank_test_player_2',
                total_score: '10.00',
                scores: [
                    {
                        category: 'Battle',
                        max_val: 20,
                        score: 0,
                        min_val: 0
                    },
                    {
                        category: 'Fair Play',
                        max_val: 5,
                        score: 5,
                        min_val: 1
                    }
                ],
                tournament_id: 'rank_test'
            })
        .toss();

    frisby.create('Non-existent tournament')
        .get(API + 'not_a_tournament/rankings', {inspectOnFailure: true})
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Tournament not_a_tournament not found in database')
        .toss();
});
