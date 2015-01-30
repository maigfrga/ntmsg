var  main = function() {
        var program = require('commander'),
            config = null;
        program
            .version('0.1.0')
            .option('-c --config <s> ',
            'specify config file location', '')
            .parse(process.argv);

        config = require(program.config);
        worker.start(config);

    },

    worker = (function() {
        var _log = null,

            _init_log = function(config) {
                console.log('starting log');
               _log = require('./logger').get_logger(config);
            },

            _start_loop = function(config) {
                var _ntsqs = require('./ntsqs')(config),
                    _ntses = require('./ntses')(config);

                setInterval(function() {
                    try {
                        _ntsqs.pull();
                        _ntses.push();
                    } catch(err) {
                        _log.error(err.name + ' ' + err.message);
                    }
                }, config.sqs.interval * 1000 );
            };

        return {
            start: function(config) {
                _init_log(config);
                _log.info('starting ntmsg');
                _start_loop(config);
            }
        }
    })();

main();
