import json
import boto3
import base64

# Initialize Polly client
polly = boto3.client('polly')

def lambda_handler(event, context):
    try:
        # Parse JSON input (text to be converted to speech)
        body = json.loads(event.get('body', '{}'))
        text = body.get('text', '').strip()

        # Validate text input
        if not text:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Allow CORS
                },
                'body': json.dumps({'error': 'Text is required'})
            }

        # Call Polly to synthesize speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'  # You can change the voice here
        )

        # Read audio stream from Polly
        audio_stream = response['AudioStream'].read()

        # Base64 encode the audio stream
        audio_base64 = base64.b64encode(audio_stream).decode('utf-8')

        # Return base64-encoded audio with proper headers
        return {
            'statusCode': 200,
            'isBase64Encoded': True,  # Ensure this flag is set to true
            'headers': {
                'Content-Type': 'audio/mpeg',  # Audio content type
                'Access-Control-Allow-Origin': '*'  # Allow CORS
            },
            'body': audio_base64  # Base64 encoded audio
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow CORS
            },
            'body': json.dumps({'error': 'Internal server error'})
        }
