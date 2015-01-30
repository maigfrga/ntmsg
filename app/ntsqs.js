module.exports = function(config) {
    var _log = require('./logger').get_logger(config),
        AWS = require('aws-sdk');

    return {
        pull: function() {
            _log.info('pulling objects from queue ');
        }
    }
};
