describe('Check that players are ranked correctly', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('Check that the rankEntries format is correct')
        .get(URL + '/rankEntries/ranking_test')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes( '0',
            {
                username: String,
                ranking: Number,
                total_score: String,
                entry_id: Number,
                scores: Array,
                tournament_id: String
            }
        )
        .expectJSONTypes('*.0.scores.*',
            {
                category: String,
                max_val: Number,
                score: Number,
                min_val: Number 
            }
        )
        .toss()


    frisby.create('Get rankings for a tournament')
        .get(URL + '/rankEntries/ranking_test')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([
            {
                username: 'homer',
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
                tournament_id: 'ranking_test'
            },
            {
                username: 'bart',
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
                tournament_id: 'ranking_test'
            },
            {
                username: 'lisa',
                ranking: 3,
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
                tournament_id: 'ranking_test'
            }
        ])
        .expectJSON('?',
            {
                username: 'maggie',
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
                tournament_id: 'ranking_test'
            }
        )
        .expectJSON('?',
            {
                username: 'marge',
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
                tournament_id: 'ranking_test'
            }
        )
        .toss();

    frisby.create('Non-existent tournament')
        .get(URL + '/rankEntries/not_a_tournament')
        .expectStatus(404)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Tournament not_a_tournament doesn\'t exist')
        .toss();
});
