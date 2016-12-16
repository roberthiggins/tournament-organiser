/* All logging should use this. You can console.log but should not */

var split = require("split"),
    winston = require("winston");

winston.emitErrs = true;

var logger = new winston.Logger({
    transports: [
        new winston.transports.File({
            level: "info",
            filename: "./log/all-logs.log",
            handleExceptions: true,
            json: true,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            colorize: false
        }),
        new winston.transports.Console({
            level: "debug", // debug and up
            handleExceptions: true,
            json: false,
            colorize: true
        })
    ],
    exitOnError: false
});

// Stream for request middleware logging
logger.stream = split().on("data", function (message) {
  logger.info(message);
});

module.exports = logger;
