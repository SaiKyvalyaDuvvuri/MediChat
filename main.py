# from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import JSONResponse
# import dbhelper


# app = FastAPI()

# @app.post("/")
# async def handle_request(request: Request):

#     payload = await request.json()

#     intent = payload ['queryResult']['intent']['displayName']
#     parameters = payload ['queryResult']['parameters']
#     output_contexts = payload ['queryResult']['outputContexts']

#     if intent == "symptom_description":
#         return  Default_Welcome_Intent(parameters)
        
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import dbhelper
import general

app = FastAPI()

inprogress_diagnosis = {}

@app.post("/")
async def handle_request(request: Request):
    
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'symptom_description':symptom_description,
        'condition_info': condition_info,
        'medical_advice': medical_advice,
        'medications': medications,
        'self_care':self_care,
        'mood_assessment':mood_management,
        'coping_strategies':coping,
        'support_resources':support,
        'add_data': save_to_db

         }

    return intent_handler_dict[intent](parameters, session_id)


#get Symptoms
def symptom_description(parameters: dict, session_id: str):
     symptom = parameters['symptom']
     condition_name = dbhelper.get_condition_name(symptom)

     if condition_name:
         fulfillment_text = f" Based on the Symptom I think you have, {condition_name}"
     else:
         fulfillment_text = f" Sorry I could not find a condition for your symptom."

  
     return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })
##

def add_to_records(parameters: dict, session_id: str):
    symptom  = parameters["symptom"]
    duration = parameters["duration"]
    severity = parameters["severity"]

    if len(records) != len(values):
        fulfillment_text = "Sorry I didn't understand. Can you please enter the details correctly?"
    else:
        new_record = dict(zip(symptom, duration, severity))

        if session_id in inprogress_diagnosis:
            current_record = inprogress_diagnosis[session_id]
            current_record.update(new_record)
            inprogress_diagnosis[session_id] = current_record
        else:
            inprogress_diagnosis[session_id] = new_record

        symptom_str = general.get_str_from_sym_dictt(inprogress_diagnosis[session_id])
        fulfillment_text = f"Patient Record inserted Successfully."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


#get condition info

def condition_info(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    condition_info = dbhelper.get_condition_info(condition_name)
    if condition_info:
        fulfillment_text = f"Here is What I know about it: {condition_info}"
    else:
        fulfillment_text = f"No condition found with order id: {condition_name}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

#get medical advice

def medical_advice(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    advice = dbhelper.get_medical_advice(condition_name)
    if advice:
        fulfillment_text = f"This is my medical Advice: {advice}"
    else:
        fulfillment_text = f"No advice found for {condition_name}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

#Get medicines
def medications(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    medicine = dbhelper.get_medication(condition_name)
    if medicine:
        fulfillment_text = f"Over the counter medication:{medicine}"
    else:
        fulfillment_text = f"No medicine found for {condition_name}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

#Get Self care tips
def self_care(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    care = dbhelper.get_self_care(condition_name)
    if care:
        fulfillment_text = f"Here are some self-care tips:{care}"
    else:
        fulfillment_text = f"No advice found for {condition_name}: {care}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def mood_management(parameters: dict, session_id: str):
     symptom = parameters['symptom']
     condition_name = dbhelper.get_condition_name(symptom)

     if condition_name:
         fulfillment_text = f" Based on mood description: {condition_name}"
     else:
         fulfillment_text = f" Sorry I could not find a condition for your symptom."

  
     return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })


def coping(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    adv  = dbhelper.get_coping_strategies(condition_name)
    if adv:
        fulfillment_text = f"Here are some Coping Strategies: {adv}"
    else:
        fulfillment_text = f"No advice found for {condition_name}: {adv}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def support(parameters: dict, session_id: str):
    condition_name = int(parameters['condition_name'])
    msupport  = dbhelper.get_condition_name(condition_name)
    if msupport:
        fulfillment_text = f"These are some of the support resources for mental health and wellness: {msupport}"
    else:
        fulfillment_text = f"No advice found for {condition_name}: {msupport}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def save_to_db(symptom: dict):
    get_next_patient_id = db_helper.get_next_patient_id()

    for symptom, severity, duration in symptom.items():
        rcode = db_helper.insert_patient_record(
            symptom,severity, duration
        )

        if rcode == -1:
            return -1

    
    return get_next_patient_id



