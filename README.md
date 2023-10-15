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

Because this API was built with limited time constraints and therefore quite basic, it should be
noted that this is not how you would do this in practice. For example, in order to stay logged in
to use the rest of the API functionality - you have to do this within the same session which isn't ideal.
If you end the session you will have to relog back in. The constraints to create a login are "user_name" and
"password" sent via a JSON.

e.g.

{
	"user_name": "UserA",
	"password": "PasswordA"
}

## Logging in:

Once you have created an account - in order to login (must be done within the same session) add your user_name and
password as part of the JSON object that you send when making requests to the API for movie searches
otherwise your request will not be authenticated.

e.g.

{
	"query": "titanic",
	"user_name": "UserA",
	"password": "PasswordA"
}

## Sending requests/pagination:

In order to access all of the data for a particular query just use the "query": "titanic" for example like in
the above. However if you want to limit the number of items the search returns and you want to skip items - i.e. not
show the first few results - you can do that as follows:

{
	"query": "titanic",
	"number_of_results_to_return": 1,
	"number_of_results_to_skip": 1,
	"user_name": "UserA",
	"password": "PasswordA"
}

Send a GET request to /search_movies endpoint.

The number of results that will be returned in this example is 1, and it will skip the first item that it returns.
If the parameters are entered wrong - it will return all of the search items. You must put both in if you want to make
that kind of limited search.

Typically with pagination - you want the user to be able to enter the page that they want and the number of results per
page. So if you wanted page 2 and 20 results per page - you would need to skip the first twenty. It didn't make sense
to do that with this API because there are not many results returned for each item. So instead - the user can select
the number of items to skip and the number of results to return.

## Saving feedback on returned queries:

If you want to save feedback on your searched queries - either with good or bad for example -you can send a POST
request to /vote_on_movies. Again, due to time constraints of the project this will need to be done in the same session.
You also need to send your user_name along with the feedback and it will look and see what the last successful query
returned to find out the film. Send a POST request to /vote_on_movies.

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

## How the functionality deals with the flakey third party API:

As there are some occasions with the third party movie API where either this results in random errors or takes
a really long time to run. Because these are rare occurrences - i.e. not likely to happen more than once the code
will just try again - there is a time limit of a second on requests before this happens. If the reason for trying 
again is because it is taking too long - there will be a time limit to make the request of a further 5 seconds - this
is because if this time limit was any shorter - too many of the requests would time out and make the application
unusable.

## How to extend the project:

In terms of deployment - I would write a docker file so that the application could be deployed to a clients server
possibly through AWS and run through docker containers as if this is being shipped to alot of clients with a different
set up this will make it much less of a headache as all the versions of libraries etc. will be uniform across all the clients
as a result of docker.

The user accounts system/log in is rudimentary at the moment and not how it would be done in practice. There needs to be
a session set up - so you login with a user name and password which gives you a session id and you pass this with each
request instead of a user name and password.

In terms of the saving a movie - you want this to be available after the user logged out when they use a new session.
Therefore these results should be stored permanently in a database.

The pagination is not set up correctly as it should really be done that you can get the items per page and set the
number of items per page to return. It wasn't necessary to do this in this example, because the search returned so few
results.

I didn't use any tools to build this as my understanding of the exercise is that you wanted to see how I write code
so it didn't seem appropriate.
