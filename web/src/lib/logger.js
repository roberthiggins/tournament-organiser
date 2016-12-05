/* All logging should use this. You can console.log but should not */

var winston = require("winston");

winston.emitErrs = true;

var logger = new winston.Logger({
    transports: [
        new winston.transports.Console({
            level: "debug", // debug and up
            handleExceptions: true,
            json: false,
            colorize: true
        })
    ],
    exitOnError: false
});

module.exports = logger;
