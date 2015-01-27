NTMSG
=========================

NTMSG is a very simple [iojs](https://iojs.org/)  application that reads email 
messages from Amazon SQS and send them through Amazon SES.
Every message represents an email to be sent to one or more
recipients, the main goal of this app is send emails keeping simplicity, for that
reason this application does not make any message process,  that means that all the messages
have to  be  formated before send them to the SQS Queue



Requirements
==================

You need a queue and a valid AWS with credentials to access SES and SQS. If you
don"t know to do it You can give a look to the links below:

* [AWS SQS Introduction](http://www.maigfrga.ntweb.co/aws-sqs-introduction/)

* [AWS SES Introduction](http://www.maigfrga.ntweb.co/introduccion-aws-ses/)


AWS Credentials
===================

This application uses  [AWS SDK for JavaScript in Node.js] (https://aws.amazon.com/sdk-for-node-js/). The best way to configure
your credentials is by creating ~/.aws/credentials file and adding the lines below:

```
    [default]
    aws_access_key_id = your_access_key
    aws_secret_access_key = your_secret_key

``

Configuration params
=======================

You need to define a config.js file on the root folder with next values:


* ["sqs"]["url"] = Queue url, it has to exists, this application doesn"t not create
the queue for you.

* ["sqs"]["interval"] = Interval in seconds to ask queue for more elements.

* ["sqs"]["max-number-of-messages"] = max number of messages to retrieve from
queue, at must 10 by request


Configuration File Example
----------------------------

```
{
    "sqs": {
        "url": "https://us-west-2.queue.amazonaws.com/63396744/myqueue",
        "interval": 10,
        "max-number-of-messages": 10
     }
}
```



Instalation
==============

```
npm install
```


Message structure
===============================

NTMGS expects json messasges, one by every email to be sent. Below a json
structure example:


```
    {
        "uuid": "95d818b8-9bd0-11e4-a124-28d2447f45b8",
        "recipients": ["user1@email.com", "user2@another.com"],
        "subject": "test message",
        "plain_text": "hello world",
        "html_text": "<hmtl><body> <h1>Hello world</h1> </hmtl></hmtl>"
    }
```







Ussage
=================
