# AI Wiki Search

A generic application for searching documents.

Uses OpenAI API, using GPT4 model.

## Setup

Add a `.env` file at the root in the following format:

```
export INSTALL_PARAMS=--set webHost=myCoolHost.net
export OPENAI_API_KEY=myKey
export SLACK_CHANNEL=slackChannelId
export SLACK_TOKEN=slackBotToken
```
 
## Building

`make build`

## Pushing

`make push`
