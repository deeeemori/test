from botocore.vendored import requests
import boto3
import json
def create_slack_payload(text):
    return {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
    ]
    }
 
def lambda_handler(event, context):
    msg = event['message']['text']
    target_language = event['callback_id']
    response_url = event['response_url']
     
    print("翻訳前：" + msg)
    print("response_url：" + response_url)
    print("callback_id：" + target_language)
    print(json.dumps(create_slack_payload(msg)))
     
    client = boto3.client('translate')
    translate_response = client.translate_text(
    Text=msg,
    SourceLanguageCode='auto',
    TargetLanguageCode=target_language
    )
     
    translated_text = translate_response["TranslatedText"]
     
    print("翻訳後：" + translated_text)
    r = requests.post(response_url, data=json.dumps(create_slack_payload(translated_text)))
    return r.json()