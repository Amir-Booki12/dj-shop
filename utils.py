
from kavenegar import *

def send_sms(phone_number,code):
    try:
       api = KavenegarAPI('51695555707A66594532597930597434646159315A635A7650473938334A484E455432743237444C4439633D')
       params = {
           'sender' : '',
           'receptor': phone_number,
           'message': f'کد تایید شما {code}'        
       }
       response = api.sms_send(params)
       print(response)
    except APIException as e: 
       print(e)
    except HTTPException as e: 
      print(e)
        
        