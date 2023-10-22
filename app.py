from flask import Flask, request
import requests
import time
from db import user_accounts, user_activity, up_or_down_vote

URL = # LINK TO  THIRD PARTY API HAS BEEN REMOVED FOR PRIVACY REASONS
# - THE PROJECT IS FOR ILLUSTRATIVE PURPOSES

app = Flask(__name__)


def error_handling_400_errors(user_query_data):
    """
    Handles 400 type errors when client makes a request
    """
    try:
        search_query = requests.get(url=URL, params=user_query_data, timeout=1)
    except Exception:
        search_query = None

    return search_query


def deal_with_pagination(user_query_data):
    """
    Deals with situation where client wants
    a certain number of items per page and
    items from a particular page
    """
    if "number_of_results_to_skip" in user_query_data:
        if "number_of_results_to_return" in user_query_data:
            limit = user_query_data["number_of_results_to_return"]
            skip = user_query_data["number_of_results_to_skip"]
            user_query_data["skip"] = skip
            user_query_data["limit"] = limit

    return user_query_data


def handle_errors_with_third_party_api(user_query_data):
    """
    Handles uncertain behaviour with third party API
    to try and give the user the best possible experience
    """
    search_query = None

    try:
        try:
            search_query = requests.get(url=URL, params=user_query_data, timeout=1)

            if str(search_query.status_code).startswith("4"):
                search_query = error_handling_400_errors(user_query_data)

        except requests.exceptions.ReadTimeout:
            search_query = requests.get(url=URL, params=user_query_data, timeout=5)

    except Exception:
        return search_query

    return search_query


def authenticate_user(user_query_data):
    """
    This will authenticate the user when they
    try to send a request
    """
    if "user_name" in user_query_data:
        if "password" in user_query_data:
            authentication_data = {
                "user_name": user_query_data["user_name"],
                "password": user_query_data["password"]
            }

            if authentication_data in user_accounts:
                return authentication_data

    return


def store_user_activity(user_name, timestamp, activity, data=None, search_query=None):
    """
    Stores user activity in the db so that we can track what the user has
    been doing with the API
    """
    if user_name in user_activity:

        activity_data = {"timestamp": timestamp, "activity": activity}

        if data and search_query:
            activity_data["data"] = data
            activity_data["result"] = search_query

        user_activity[user_name].append(activity_data)


@app.post("/vote_on_movies")
def store_up_or_down_vote_of_movies():
    """
    The user after they have immediately received a response
    with data can store what they thought of the results
    via this endpoint
    """
    user_data = request.get_json()
    user_name = request.get_json().get("user_name")
    feedback = request.get_json().get("feedback")

    try:
        info_to_save = user_activity[user_name][-1]["result"]["items"]
    except Exception:
        info_to_save = None

    if user_name not in up_or_down_vote:
        up_or_down_vote[user_name] = []

    if info_to_save and feedback:
        for info in info_to_save:
            info["rating"] = user_data["feedback"]

            up_or_down_vote[user_name].append(info)

            return user_data, 200
    else:
        return {"Error": "Invalid data/ data in wrong format/previous session has already ended, please try again"}, 200


@app.get("/vote_on_movies")
def retrieve_rated_movies_for_user():
    """
    A way for the user to retrieve previously
    rated movies from the search
    """
    user_query_data = request.get_json()

    if "user_name" in user_query_data:
        if user_query_data["user_name"] in up_or_down_vote:
            return {"movie_ratings": up_or_down_vote[user_query_data["user_name"]]}, 200

    return {"Results": "No previous history found"}, 200


@app.post("/create_user_account")
def create_user_account():
    """
    Creates user accounts so user can log in
    """
    user_data = request.get_json()
    if user_data not in user_accounts:
        if ("user_name" and "password") in user_data.keys():
            user_accounts.append(user_data)
            user_activity[user_data["user_name"]] = []
            return {"Account Created!": user_data}, 200

    return {"Error": "Account not created, please include user_name and password ONLY if not already logged in"}, 401


@app.get("/search_movies")
def search_movies():
    """
    Allows users to search for movies using the API
    by first authenticating the user - if they are not
    logged in - they cannot search for movies. User
    activity is also stored
    """
    user_query_data = request.get_json()
    authentication = authenticate_user(user_query_data)
    time_stamp = time.time()

    if authentication:

        user_name = authentication["user_name"]
        paginated_user_query = deal_with_pagination(user_query_data)
        search_query = handle_errors_with_third_party_api(paginated_user_query)

        if search_query:

            query_results = search_query.json()

            store_user_activity(user_name, time_stamp, "successful_query", user_query_data, query_results)

            query_results["message"] = "Did you like this movie selection? To upvote send feedback: good  or " \
                                       "feedback: bad with your user_name: your name to /vote_on_movies end point now "
            return query_results, 200
        else:
            store_user_activity(user_name, time_stamp, "time_out_error")
            return {"Error": "Query has timed out, please try again"}, 504

    else:
        return {"Error": "Authentication failed, please send valid user_name and password credentials"}, 401
