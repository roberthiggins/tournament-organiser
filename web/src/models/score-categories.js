var emptyCategory = function() {
    return {
        "name": "",
        "percentage": "",
        "per_tournament": false,
        "min_val": "",
        "max_val": "",
        "zero_sum": false,
        "opponent_score": false
        };
};

// Sanitise score-categories for POSTing
var cleanCategories = function(cats) {
    var cleanedCategories = (cats || [])
        .map(function booleanConversion(cat) {
            var result = {};
            for (var key in cat) {
                if (cat[key] === "false") {
                    result[key] = false;
                }
                else if (cat[key] === 'true') {
                    result[key] = true;
                }
                else {
                    result[key] = cat[key];
                }
            }
            return result;
            })
        .map(function stripUnusedFields(cat) {
            var result = {},
                proto = emptyCategory();

            for (var key in proto) {
                result[key] = cat[key];
            }
            return result;
            })
        .filter(function stripEmptyCats(cat) {
            var empty = emptyCategory();
            for (var key in empty) {
                if (cat[key] !== empty[key]) {
                    return true;
                }
            }
            return false;
            });

    var reqFields = ["name", "percentage", "min_val", "max_val"];
    cleanedCategories
        .forEach(function checkRequired(cat) {
            reqFields.forEach(function(key) {
                if ((cat[key] || "") === "") {
                    throw "Please fill in all fields";
                }
            });
        });

    return cleanedCategories;
};

exports.cleanCategories = cleanCategories;
exports.emptyScoreCategory = emptyCategory;
