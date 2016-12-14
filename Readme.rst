NTMSG
=========================

NTMSG is a python application that reads email
messages from a Queue (Amazon SQS and Postgres backend supported)
and send them through [mailgun](http://www.mailgun.com/) .

Every message represents an email to be sent to one or more
recipients, the main goal of this app is send emails keeping simplicity, for that
reason this application does not make any message process,  that means that all messages
have to be formatted before to be sent them to the Queue



Requirements
==================

You need a queue and a valid AWS with credentials to access SES and SQS. If you
don"t know to do it You can give a look to the links below:

* [Flask utils](https://github.com/maigfrga/flaskutils)

* [Sqlalchemypostgresutils] (https://github.com/maigfrga/sqlalchemypostgresutils)

* [AWS SQS Introduction](http://www.maigfrga.ntweb.co/aws_sqs_introduction/)


Instalation
==============

```
sudo pip3 install -r tools/requirements.txt
```


Configuration params
=======================

INTERVAL
-------------

Interval in seconds to ask queue for more elements, default value is 1 second:

```
INTERVAL = 1
```

MAX_NUMBER_OF_MESSAGES
---------------------------

Max number of messages to retrieve from queue, at must 10 by request, by default
1:

```
MAX_NUMBER_OF_MESSAGES = 1
```

QUEUE_BAKEND
---------------------------

POSTGRES AND AWS SQS backend are supported, 
in order to use postgres, following configuration params
should be added to the configuration file:

```
QUEUE_BAKEND = 'POSTGRES'

POSTGRESQL_DATABASE_URI = 'postgresql://ds:dsps@localhost:5432/ds'
```

To use AWS SQS following configuration parameters should be added:

```
QUEUE_BAKEND = 'AWS_SQS'
AWS_SECRET_ACCESS_KEY=asdjfl
AWS_ACCESS_KEY_ID=34lsdfjafd
SQS_URL = '' # Queue url, it has to exists, this application doesn"t not create the queue for you.
AWS_REGION = 'us_west_2' # aws were queue is allocated.
```

if you don't want to expose your AWS credentials in the configuration file, you
can export them as variables:

```
export AWS_SECRET_ACCESS_KEY=asdjfl
export AWS_ACCESS_KEY_ID=34lsdfjafd
```

LOGGER
--------------------------


```
LOGGER = {
    'file': True,
    'filename': '/var/log/ntmsg.log',
    'console': True
}
```



Message structure
===============================

NTMGS expects json messages, one by every email to be sent. Below a json
structure example:


```
    {
        "from": "sender@email.com",
        "to": ["user1@email.com", "user2@another.com"],
        "subject": "test message",
        "text": "hello world",
        "html": "<h1>Hello world</h1>",
        "reply_to": ["email1@mydomain.com", "email2@mydomain.com"]
    }
```



MAILGUN_API_KEY
----------------------


```
MAILGUN_API_KEY = 'my_key'
```


Usage
================


Pushing a message to the queue:

```
python3 manage.py push --config config.production --msg '{ 
        "from": "sender@email.com",                        
        "to": ["user1@email.com", "user2@another.com"],    
        "subject": "test message",                         
        "text": "hello world",                             
        "html": "<h1>Hello world</h1>",                    
        "reply_to": ["email1@mydomain.com", "email2@mydomain.com"] 
    }'
```





Resources
====================

* [Amazon SQS Documentation](http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html)

* [Mailgun Documentation](https://documentation.mailgun.com/quickstart.html)
