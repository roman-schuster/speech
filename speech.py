from papirus import PapirusText                     # PaPiRus e-ink display python library
import argparse                                     # for getting the wav file from command line
import base64                                       # for encoding the wav file to send to Google Speech API
import json                                         # for unwrapping the Google Speech API response
import httplib2                                     # for sending the Google Speech API request

def get_speech_service():
    '''
    Uses application default credentials to authorize google api requests
    Note that environment variables:
        GOOGLE_APPLICATION_CREDENTIALS must be set to the path of service credentials json
        GCLOUD_PROJECT must be set to the name of your project
        * I did this in the bash file *
    Returns:
        Google Cloud Speech API service
    '''
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
        
def main(speech_file):
    '''
    Transcribe the given audio file, translates it, and prints it out
    Args:
        speech_file: the name of the audio file.
    '''
    with open(speech_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'linear16',
                'sampleRate': 16000,
                'languageCode': 'en-US',
                'profanityFilter': False,
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    
    response = service_request.execute()
    
    # Unwrapping the json
    result_string = '' # The final string containing the text we translated
    json_results = json.dumps(response)
    results = json.loads(json_results)['results']
    for result in results:
        alternatives = result['alternatives']
    
        for alternative in alternatives:
            transcript = alternative['transcript']
        
            for i in range(len(transcript)):
                result_string += transcript[i]
                
    text = PapirusText()
    text.write(result_string)
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='/home/pi/speech.wav')
    args = parser.parse_args()
    main(args.speech_file)