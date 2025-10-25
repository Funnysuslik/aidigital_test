### PLAN 
1. Need to write class for API request from https://restcountries.com/v3.1/all endpoint (!You **must** specify the fields you need (up to 10 fields) when calling the `all` endpoints, otherwise you’ll get a `bad request` response. )*

you must choose most important fields and add them to the default endpoint constant. Optionally add variable for fields with starting script (?) don’t see implementation rn, need think about it.**

1.2 add model to verify response in case of incidents or API changes with pydentic (use sqlmodel) 
but in the task explicitly said that result should be dataframe instance of pandas lib***

2 write data to the PostgreSQL via ORM (?)(find which)

2.1 add infra - docker-compose with at least psql and plotly in advance.

2.2 think if i need alembic SQLmodel e.t.c.

3 write simple plotly app 

3.1 Create a visualization - it should include a table with data and block with flags.

3.2 Table should support sorting and include all data you have saved to database.

3.3 Block with flags should display flag of the country selected in the table right now (flag urls are available from the API).

4 add settings to collect constants from .env

5 add .env generation with google secrets service (how it called?)

6 add logger to log success requests and fails

8 add redis server to store recently collected requested fields?

9 in plotly should present 3 sources for data to build data visualization (table): 1 - Redis 2 - DB 3 - data collection script from step 1

10 basic rabitmq tasks for different sources of data.

* You can specify which fields to retrieve. The fields parameter will give autocomplete suggestions. Full list of available fields:

`name`: Object with common, official, and native names

`tld`: Top-level domain

`cca2`, `ccn3`, `cca3`, `cioc`: Country codes

`independent`: Boolean flag

`status`: Status of the country

`unMember`: UN membership status

`currencies`: Currency information

`idd`: International dialing info

`capital`: Capital city

`altSpellings`: Alternative spellings

`region`, `subregion`: Region info

`languages`: Languages spoken

`translations`: Translations of country name

`latlng`: Latitude and longitude

`landlocked`: Boolean flag

`borders`: Bordering countries

`area`: Area in square kilometers

`demonyms`: Demonyms

`flag`: Emoji flag

`maps`: Google and OpenStreetMap links

`population`: Population count

`gini`: GINI coefficient

`fifa`: FIFA code

`car`: Car signs and driving side

`timezones`: List of timezones

`continents`: List of continents

`flags`: Object with PNG and SVG flag URLs

`coatOfArms`: Coat of arms images

`startOfWeek`: Start of the week

`capitalInfo`: Capital coordinates

`postalCode`: Postal code format

**  1. The code should be production-ready, so use your best practices. If there is something you want to point out, or something that you paid special attention to when working with this API, feel free to write comments in the code, they will be appreciated.

*** As a result of this step you should have a code to receive data into pandas dataframe.
