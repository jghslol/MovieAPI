# API to interact with third party movie API

API that talks to third party movie API and returns data regarding movie searches.

Requirements:

The following libraries needs to be installed:

1) Flask
2) Requests
3) Time

How to use the API and functionality:

To run the application:

• Open a terminal and run the following command: flask run --port 5001

• Get a tool like Insomnia in order to send requests to the API.

## Creating an Account:

There is a login system where the user has to create an account by sending a POST request
to the API - via this endpoint - /create_user_account. 

The constraints to create a login are "user_name" and
"password" sent via a JSON.

e.g.

{
	"user_name": "UserA",
	"password": "PasswordA"
}

## Logging in:

Once you have created an account - in order to login (must be done within the same session) add your user_name and password as part of the JSON object that you send when making requests to the API for movie searches
otherwise your request will not be authenticated.

e.g.

{
	"query": "titanic",
	"user_name": "UserA",
	"password": "PasswordA"
}

## Sending requests/pagination:

In order to access all of the data for a particular query just use the "query": "titanic" for example like in
the above. However if you want to limit the number of items the search returns and you want to skip items - i.e. not show the first few results - you can do that as follows:

{
	"query": "titanic",
	"number_of_results_to_return": 1,
	"number_of_results_to_skip": 1,
	"user_name": "UserA",
	"password": "PasswordA"
}

Send a GET request to /search_movies endpoint.

The number of results that will be returned in this example is 1, and it will skip the first item that it returns.
If the parameters are entered wrong - it will return all of the search items. You must put both in if you want to make that kind of limited search.

## Saving feedback on returned queries:

If you want to save feedback on your searched queries - either with good or bad for example -you can send a POST
request to /vote_on_movies. Again, due to time constraints of the project this will need to be done in the same session.
You also need to send your user_name along with the feedback and it will look and see what the last successful query returned to find out the film. Send a POST request to /vote_on_movies.

e.g.

{
	"feedback": "good",
	"user_name": "UserA"
}

## Getting back your previous saved feedback on the movie:

Again in the same session. If you want to retrieve the movies the you have rated you can send a GET request to 
/vote_on_movies end point. You only need to send a JSON object with your user_name e.g:

{
	"user_name": "UserA"
}
