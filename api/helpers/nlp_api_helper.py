from api import interpreter, last_status, information, start_time
import datetime

def processing(message):
  print(message)
  global last_status, information, start_time
  if datetime.datetime.now().timestamp() - start_time.timestamp() > 5:
    start_time = datetime.datetime.now() 
    # message = preprocess(message)
    nlu_response = interpreter.parse(message)
    if last_status == 0:
      information = {}
      if nlu_response['intent']['confidence'] > 0.5:
        intent = nlu_response['intent']['name']
        if intent == 'interview_query':
          last_status = 1
          entities = nlu_response['entities']
          for entity in entities:
            if entity['entity'] == 'time':
              information['time'] = entity['value']
              return 'interview_guest_name'
          return 'interview_time'       
        else:
          last_status = 0
      else:
        intent = 'other'
        last_status = 0
      return intent
    else:
      if 'time' not in information:
        information['time'] = message
        return 'interview_guest_name'
      if 'guest_name' not in information:
        information['guest_name'] = message
        return 'interview_responsibility'
      elif 'responsibility' not in information:
        information['responsibility'] = message
        last_status = 0
        return 'interview_query_complete'
  else:
    return 'noise'
