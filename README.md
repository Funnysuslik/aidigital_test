# RestCountries Data Service (Test task for AI digital)

A small project demonstrating data collection, storage, and visualization based on the [RestCountries API](https://restcountries.com/).
The goal is to build a simple, production-style pipeline using Python, Pandas, PostgreSQL, Dash.

---

## How to Run

```bash
sh entrypoint.sh
```

---

## Further Ideas

### Testing

* Implement tests for both the application and the scraper components.

### Scraper

* To populate the database, currently you must run `scraper.main()` manually.
  At the moment it's hardcoded for RestCountries.
* In the future, consider adding scripts for each processing step and storing them in dedicated directories.
  And run scraper in case of need for certain source
* Add data validations — at least for trusted and well-known data sources.

### Database

* Define mandatory fields and add indexes to improve query performance — at least for trusted and well-known data sources.

### Application

* Migrate to a more flexible and powerfull framework.

* Add caching (Redis service is easy to set up; decorators can be used for cache logic to keep code DRY).

* Implement a data fetching strategy:

  ```
  Redis → DB → Scraper
  ```

* Implement on-demand field collection instead of loading everything at startup.
  For large datasets, consider queueing scraper tasks via Kafka or RabbitMQ.

---

## Project Plan

### 1. API Client

* Write a class for requests to the `https://restcountries.com/v3.1/all` endpoint.
  **Note:** You must specify the required fields (up to 10) when calling the `all` endpoint — otherwise, it returns a Bad Request.
* Choose the most important fields and store them in a default constant.
* Optionally, add a variable to specify fields dynamically when starting the script.
* (?) Validate the response using Pydantic (or SQLModel) to detect API changes or errors.
  However, the final result must be a `pandas.DataFrame` instance.

---

### 2. Database

* Write collected data to PostgreSQL via an ORM (decide which to use — e.g., SQLModel or SQLAlchemy).
* Infrastructure:

  * Add `docker-compose` with at least:

    * PostgreSQL
    * Plotly (for visualization, in advance)
* Decide whether to include Alembic for migrations.

---

### 3. Plotly Visualization

* Build a simple Plotly app:

  * Display a table with the saved country data.
  * Add a flag block showing the currently selected country.
* Requirements:

  * The table must support sorting and display all saved fields.
  * The flag should update dynamically based on the selected table row.

---

### 4. Configuration

* Use a `.env` file for configuration constants.
* Add automatic `.env` generation from Google Secret Manager (confirm the exact service name).

---

### 5. Logging

* Add a logger to record successful and failed API requests.

---

### 6. Caching

* Add a Redis service to store recently collected or requested fields.

---

### 7. Data Sources

Plotly should be able to visualize data from three sources:

1. Redis
2. Database
3. Scraper (real-time API request)

---

### 8. Message Queue

* Implement basic RabbitMQ tasks for different data sources.

---

## Available API Fields

You can specify which fields to retrieve (up to 10).
Full list of available fields:

`name`, `tld`, `cca2`, `ccn3`, `cca3`, `cioc`, `independent`, `status`, `unMember`,
`currencies`, `idd`, `capital`, `altSpellings`, `region`, `subregion`,
`languages`, `translations`, `latlng`, `landlocked`, `borders`, `area`,
`demonyms`, `flag`, `maps`, `population`, `gini`, `fifa`, `car`, `timezones`,
`continents`, `flags`, `coatOfArms`, `startOfWeek`, `capitalInfo`, `postalCode`
