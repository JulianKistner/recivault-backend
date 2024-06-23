# Recivault Backend

This is the backend service for recivault. It provides an API with endpoints to manage receipts and 
store them in the database. 

## Environemnt 
- Python 3.12.2

The project uses Pipenv to use a virtual environment for the installed packages. All packages are defined 
in the Pipefile. 

### Start 

1. Checkout project 
2. create pipenv environment if it doesnt exist
   1. Create environment with ide 
   2. (optional) Create environment with console `pipenv install`
3. Start environment with `pipenv shell`
4. Install all packages with `pipenv install`
5. Create run configuration and set all environment variables 

### Environment variables

| Variable Name          | Description                                                      | Example                                                                        |
|------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------|
| DATABASE_URI           | URI with address and login for postgresql database               | postgresql+psycopg2://<username>:<password>@<domain>:5432/<database_name>      |
| KEYCLOAK_SERVER_URL    | URL to used keycloak instance (base url)                         | https://accounts.recivault.com/                                                |
| KEYCLOAK_REALM         | Name of the used Keycloak realm                                  | recivault                                                                      |
| KEYCLOAK_CLIENT_ID     | Public client id to identify the application                     | recivault-client                                                               |
| KEYCLOAK_CLIENT_SECRET | Private client secret to identify the application (not required) |                                                                                |
| KEYCLOAK_AUTH_URL      | Auth endpoint to login                                           | https://accounts.recivault.com/realms/recivault/protocol/openid-connect/auth   |
| KEYCLOAK_TOKEN_URL     | Token endpoint to request a valid token                          | https://accounts.recivault.com/realms/recivault/protocol/openid-connect/token  |

### Dependencies 

- Database (PostgreSQL) 

The application requires a running database with full crud permissions to create, update and delete 
database entries. The database must contain all database tables that are contained in the DB model 
of the documentation. If the tables do not exist, runtime errors may occur. 

- Keycloak 

The system requires a valid installed and configured keycloak instance. Otherwise the endpoints would 
not work.

## API 

- local environment: `http://localhost:5000` 
- swagger documentation: `http://localhost:5000/api`

The api required for all endpoint a valid jwt. (excluding only the health and version endpoint)

## Hosted instance 

A complete instance of recivault backend with a database and keycloak is running on a server. It can be 
accessed via the following points: 
- Backend: `https://api.recivault.com/api`
- Keycloak: `https://accounts.recivault.com`



