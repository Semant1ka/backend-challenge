# backend-challenge

Hello there! :wave:

This is our challenge for potential new backend developer team members. We'd like to see how you tackle a greenfield development project in Ada's domain (chat). We don't mind what language you use to complete the challenge. Feel free to try something new, or to use technology that you're already comfortable with. That being said, we're partial to Python here at Ada :smile:

We'd like you to design and build a simple web service responsible for two things:

1. Accept incoming chat messages over HTTP
2. Serve up conversation history over HTTP

## Specifications

Your solution should start an HTTP service on any port you'd like. Please include instructions on how to start your service (so that we can test the functionality!)

### `/messages/` Resource

The `/messages/` resource accepts HTTP POST actions to create new messages in the conversation. A typical message resource has the format of:

```javascript
{
    "sender": "anson",
    "converstaion_id": "1234",
    "message": "I'm a teapot"
}
```

Here, `"sender"` is a string username, `"conversation_id"` is a unique identifier for a particular conversation, and `"message"` is a string message to be logged to a conversation.

### `/conversations/<conversation_id>` Resource

The `/conversations/<conversation_id>` resource accepts an HTTP GET action and returns a list of conversation messages. A typical conversation as the format of:

```javascript
{
    "id": "1234",
    "messages": [
        {
            "sender": "anson",
            "message": "I'm a teapot",
            "created": "2018-01-17T04:50:14.883Z"
        },
        {
            "sender": "david",
            "message": "Short and stout",
            "created": "2018-01-17T04:52:17.201Z"
        }
    ]
}
```

Here, a conversation with two messages is presented.

## Notes
- You can assume that the entities sending incoming chat messages are authenticated and trustworthy (authentication is outside of the scope of this project)
- Feel free to use any technology that you'd like, though we recommend Python
- We definitely don't want you to spend too much time on this!
