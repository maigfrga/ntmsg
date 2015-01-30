module.exports = function(config){
    var _log = require('./logger').get_logger(config),
       AWS = require('aws-sdk');

    return {
        push: function() {
            _log.info('sending email');
        }
    }
};
