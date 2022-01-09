# importing libraries
from flask import Flask, request, Response, jsonify
import pandas as pd

app = Flask(__name__)

data = pd.read_csv("rest.csv")


def fetch_json():
    conditions = trials['Conditions']
    inventions = trials['Interventions']
    locations = trials['Locations']
    status = trials['Status']
    study_title = trials['Study Title']
    return conditions, inventions, locations, status, study_title


def get_list_of_ids():
    lis = []
    for i in data["Id"]:
        lis.append(i)
    return lis


@app.get("/trials/<int:id>")
def get_trials(id):
    try:
        data.set_index("Id", inplace=True)
        response = data.loc[id].to_dict()
        return response, 200
    except Exception as e:
        print(e)


@app.post("/trials")
def add_trials():
    global data, trials
    if request.is_json:
        trials = request.get_json()
        add_id = trials["Id"]
        add_condition, add_invention, add_location, add_status, add_study_title = fetch_json()
        dataframe = {'Id': add_id, 'Conditions': add_condition, 'Interventions': add_invention,
                     'Locations': add_location, 'Status': add_status, 'Study Title': add_study_title}
        data = data.append(dataframe, ignore_index=True)
        data.to_csv("rest.csv")

        return "Data added into dataframe",  201
    else:
        return {"error": "Request must be JSON"}, 415


@app.route('/update_trials/<int:id>', methods=['POST'])
def update_trial(id):
    global data, trials
    try:
        list_of_ids = get_list_of_ids()
        if id in list_of_ids:
            data.set_index("Id", inplace=True)
            trials = request.get_json()
            update_id = id
            update_condition, update_invention, update_location, update_status, update_study_title = fetch_json()
            data.at[update_id, 'Study Title'] = update_study_title
            data.at[update_id, 'Conditions'] = update_condition
            data.at[update_id, 'Interventions'] = update_invention
            data.at[update_id, 'Locations'] = update_location
            data.at[update_id, 'Status'] = update_status
            data.reset_index(inplace=True)
            data.to_csv("rest.csv")
            response = jsonify('Dataframe updated!')
            return response,  200
        else:
            response = jsonify('This id is not present in our csv')
            return response, 200
    except Exception as e:
        print(e)


@app.route('/delete_trials/<int:id>', methods=['DELETE'])
def update_trial(id):
    global data
    try:
        list_of_ids = get_list_of_ids()
        if id in list_of_ids:
            data.set_index("Id", inplace=True)
            trials = request.get_json()
            trial_id = id
            data = data.drop(id)
            data.reset_index(inplace=True)
            data.to_csv("rest.csv")
            response = jsonify('trial deleted!')
            response.status_code = 200
            return response
        else:
            response = jsonify('This id is not present in our csv')
            return response, 200

    except Exception as e:
        print(e)
