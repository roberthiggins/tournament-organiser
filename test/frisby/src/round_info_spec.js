describe('HTTP Method Test Suite', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR,
        auth = function(user, pass){
            return "Basic " + new Buffer(user + ":" + pass).toString("base64");
        };

    frisby.create('POST 2 rounds to setup')
        .post(API + 'tournament/round_test/rounds', {
            numRounds: 2
        }, {json: true})
        .addHeader('Authorization', auth('superuser', 'password'))
        .expectStatus(200)
        .after(function(){
            frisby.create('POST 2 missions to setup')
                .post(API + 'tournament/round_test/missions', {
                    missions: ['mission_1', 'mission_2']
                }, {json: true})
                .addHeader('Authorization', auth('superuser', 'password'))
                .expectStatus(200)
                .after(function(){
                    frisby.create('Check those missions exist')
                        .get(API + 'tournament/round_test/rounds/1')
                        .expectStatus(200)
                        .expectJSONTypes({
                            draw: Array,
                            mission: String
                        })
                        .expectJSON({
                            draw: Array,
                            mission: 'mission_1'
                        })
                        .toss();
                    frisby.create('Check those missions exist')
                        .get(API + 'tournament/round_test/rounds/2')
                        .expectStatus(200)
                        .expectJSONTypes({
                            draw: Array,
                            mission: String
                        })
                        .expectJSON({
                            draw: Array,
                            mission: 'mission_2'
                        })
                        .toss();
                })
                .toss();
        })
        .toss();

    frisby.create('TO auth')
        .post(API + 'tournament/round_test/rounds', {
            numRounds: 2
        }, {json: true})
        .addHeader('Authorization', auth('round_test_to', 'password'))
        .expectStatus(200)
        .toss();
    frisby.create('No auth')
        .post(API + 'tournament/round_test/rounds', {
            numRounds: 2
        }, {json: true})
        .expectStatus(401)
        .expectBodyContains('Could not verify your access level')
        .toss();
    frisby.create('Bad auth')
        .post(API + 'tournament/round_test/rounds', {
            numRounds: 2
        }, {json: true})
        .addHeader('Authorization', auth('enter_score_entry_1', 'password'))
        .expectStatus(401)
        .expectBodyContains('Could not verify your access level')
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/foo/rounds/1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/4')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/-1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/1/rounds/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/1/1')
        .expectStatus(404)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/1/rounds/1')
        .expectStatus(400)
        .toss();
});
