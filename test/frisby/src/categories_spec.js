'use strict';
describe('HTTP Method Test Suite', function () {
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('GET from non-existent tournament')
        .get(API + 'tournament/not_a_thing/score_categories')
        .expectStatus(400)
        .toss();

    frisby.create('GET from non-existent tournament')
        .get(API + 'tournament//score_categories')
        .expectStatus(404)
        .toss();


    // Normal function of getting categories
    frisby.create('set the score categories for category_test')
        .post(API + 'tournament/category_test/score_categories', {
            categories: ['categories_0', 'categories_1'],
            categories_0: ['categories_test_one', 8, true, 4, 12],
            categories_1: ['categories_test_two', 13, false, 3, 11]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .toss();
    frisby.create('GET a list of tournament categories')
        .get(API + 'tournament/category_test/score_categories')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes('0', {
            'id': Number,
            'name': String,
            'percentage': Number,
            'per_tournament': Boolean,
            'min_val': Number,
            'max_val': Number
        })
        .expectJSON([
            {
                'id': Number,
                'name': 'categories_test_one',
                'percentage': 8,
                'per_tournament': true,
                'min_val': 4,
                'max_val': 12
            },
            {
                'id': Number,
                'name': 'categories_test_two',
                'percentage': 13,
                'per_tournament': false,
                'min_val': 3,
                'max_val': 11
            }
        ])
        .toss();


    // Modify the categories
    frisby.create('set the score categories for category_test')
        .post(API + 'tournament/category_test/score_categories', {
            categories: ['categories_3'],
            categories_3: ['categories_test_three', 99, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .toss();
    frisby.create('GET a list of tournament categories')
        .get(API + 'tournament/category_test/score_categories')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([
            {
                'id': Number,
                'name': 'categories_test_three',
                'percentage': 99,
                'per_tournament': true,
                'min_val': 1,
                'max_val': 2
            }
        ])
        .toss();


    // Empty the categories
    frisby.create('set the score categories for category_test to none')
        .post(API + 'tournament/category_test/score_categories', {
            categories: []
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .toss();
    frisby.create('GET categories from now empty tournament')
        .get(API + 'tournament/category_test/score_categories')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();


    // Modify the categories incorrectly
    frisby.create('Incorrect: categories don\'t match')
        .post(API + 'tournament/category_test/score_categories', {
            categories: ['categories_3'],
            categories_1: ['categories_test_no_match', 5, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create('Incorrect: No names')
        .post(API + 'tournament/category_test/score_categories', {
            categories_1: ['categories_test_no_names', 5, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create('Incorrect: No category info')
        .post(API + 'tournament/category_test/score_categories', {
            categories: ['categories_3']
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();


});
