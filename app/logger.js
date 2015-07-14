module.exports = (function() {
    var winston = require('winston');

    return {
        get_logger: function(config) {
            var logger = {},
                transports = [
            ];

            if (config.logger.file) {
                transports.push(new (winston.transports.File)({ filename: config.logger.filename }));
            }

            if(config.logger.console) {
                transports.push(new (winston.transports.Console)());
            }

            logger = new (winston.Logger)({
                transports: transports
            });

            return logger;
        }
    };
})();
