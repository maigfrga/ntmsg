module.exports = function(config) {
    var AWS = require('aws-sdk'),

        _sqs = null,

        _sqs_params = {},

        _ses_params = {},

        _ses = null,

        _log = require('./logger').get_logger(config),

        _queue_url = config.sqs['url'],

        _init_aws = function() {
            AWS.config.region = config.aws.region;
            _sqs = new AWS.SQS();
            _ses = new AWS.SES();
            _sqs_params = {
                QueueUrl: config.sqs.url,
                MaxNumberOfMessages: config.sqs['max-number-of-messages'],
                WaitTimeSeconds: 0
             };
        },

        _ses_callback = function(err, data) {
            if (err) {
                _log.error('_ses_callback ' + err.message);

            } else {
                _log.info('_ses_callback success: ');
                _log.info(data);
            }
        },

        _push_ses = function(msg) {
            // http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SES.html#sendEmail-property
            try {
                _log.info('push ses message with uuid %s', msg.uuid);
                var params = {
                    'Destination':  {
                        'ToAddresses': msg.to
                     },
                    'Message': {
                        'Body': {
                            'Html': {
                                'Data': msg.html,
                                'Charset': 'utf-8'
                            },
                            'Text': {
                                'Data': msg.text,
                                'Charset': 'utf-8'
                            }
                        },
                        'Subject': {
                            'Data': msg.subject,
                            'Charset': 'utf-8'
                        }
                    },
                    'Source': msg.from,
                    'ReplyToAddresses': msg.reply_to
                };
                _ses.sendEmail(params, _ses_callback);

            } catch(err) {
                _log.error('_push_ses ' + err.name + ' ' + err.message);
            }
        },

        _process_sqs = function(err, data) {
            // Callback function from receiveMessage
            if (err) {
                _log.error('_process_sqs ' + err.message);

            } else {
                var msg_body = {};
                _log.info('SQS requestId %s', data.ResponseMetadata.RequestId);

                if (data.Messages !== undefined ) {
                    for (var i=0; i< data.Messages.length; i++) {
                        msg_body = JSON.parse(data.Messages[i]['Body']);
                        _push_ses(msg_body);
                    }

                } else {
                    _log.info('_process_sqs No messages available')
                }
            }

        },

        _pull_sqs = function(){
            // http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html#receiveMessage-property
            _log.info('_pull_sqs  requesting objects from queue');
            _sqs.receiveMessage(_sqs_params, _process_sqs);
        };

    return {
        pull: function() {
            _init_aws(),
            _pull_sqs();
        }
    }
};
