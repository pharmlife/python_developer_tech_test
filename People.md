# Welcome to the People's API specification

  * [Storage]
    * You are free to choose how to storage permanent data. As way to help, a basic SQLite database has included in this repository.
  * [Authentication Endpoints] 
    * A x-api-token must be provided in the headers for EVERY endpoint but /status. If the user doesn't provide any token, you should return a 401 status code. You can assume any value provided is a valid token.

  * [Data Endpoints](#data-endpoints)  
    - [/people](#people)
        - [GET](#list-people)  
        - [POST](#create-person)  
        - [DELETE](#delete-person)  
    - [/people/<person:id>/alias](#aliases)  
        - [POST](#create-alias)  
        - [GET](#list-aliases)  
    - [/status](#status)

### people

#### List people
* **URI** : `/people`
* **METHODS** : `GET`
* **REQUIRED HEADERS**:
    - `x-api-key: <auth token>`
* **SUCCESS RESPONSE**
    * **CODE**: 200
    * **TEXT**: `[{"id":<owner id>, "name": <owner name>}, ...]`
* **FAILURE RESPONSE**
    * **CODE**: 401
    * **TEXT**: `{"error": "Authorization required"}`
* **SAMPLE CALL**  
`curl -x GET ${SERVER}/people -H 'x-api-key: ${TOKEN}'`

#### Create person
* **URI** : `/people`
* **METHODS** : `POST`
* **CONTENT-TYPE**: `JSON`
* **REQUIRED PARAMS**:
    - `name=[string]`
* **REQUIRED HEADERS**:
    - `x-api-key: <auth token>`
* **SUCCESS RESPONSE**
    * **CODE**: 201
    * **TEXT**: `{"id": <new id>, "name": <new name>}`
* **FAILURE RESPONSE**
    * **CODE**: 400
    * **TEXT**: `{"error": "Names must be alphanumeric"}`  
    OR  
    * **CODE**: 401
    * **TEXT**: `{"error": "Unauthorised"}`  
    OR  
    * **CODE**: 409
    * **TEXT**: `{"error": "Name exists"}`  
* **SAMPLE CALL**  
`curl ${SERVER}/people -H 'x-api-key: ${TOKEN}' -H 'Content-Type: application/json -d {"name": ${NAME} }`

#### Delete person
* **URI** : `/people/<int:person id>`
* **METHODS** : `DELETE`
* **REQUIRED HEADERS**:
    - `x-api-key: <auth token>`
* **SUCCESS RESPONSE**
    * **CODE**: 204
    * **TEXT**: `null`
* **FAILURE RESPONSE**
    * **CODE**: 401
    * **TEXT**: `{"error": "Unauthorised"}`  
    OR  
    * **CODE**: 404
    * **TEXT**: `{"error": "Not Found"}`
* **SAMPLE CALL**  
`curl ${SERVER}/people/${OWNER ID} -X DELETE -H 'x-api-key: ${TOKEN}'`


### Aliases

#### List Aliases
* **URI** : `/people/<int person>/alias`
* **METHODS** : `GET`
* **REQUIRED HEADERS**:
    - `x-api-key: <auth token>`
* **SUCCESS RESPONSE**
    * **CODE**: 200
    * **TEXT**: `[<name>, ...]`
* **FAILURE RESPONSE**
    * **CODE**: 401
    * **TEXT**: `{"error": "Unauthorised"}`
* **SAMPLE CALL**  
`curl ${SERVER}/people/1/aliases -H 'x-api-key: ${TOKEN}'`

#### Create Alias
* **URI** : `/people/<int person>/alias`
* **METHODS** : `POST`
* **CONTENT-TYPE**: `JSON`
* **REQUIRED PARAMS**:
    - `name=[string]`
* **REQUIRED HEADERS**:
    - `Cookie: <auth token>`  
    OR
    - `x-api-key: <auth token>`
* **SUCCESS RESPONSE**
    * **CODE**: 201
    * **TEXT**: `{"id": <new id>}`
* **FAILURE RESPONSE**
    * **CODE**: 400
    * **TEXT**: `{"error": "Names must be alphanumeric"}`  
    OR  
    * **CODE**: 403
    * **TEXT**: `{"error": "Unauthorised"}`  
    OR  
    * **CODE**: 409
    * **TEXT**: `{"error": "Name exists"}`  
* **SAMPLE CALL**  
`curl ${SERVER}/cats -H 'x-api-key: ${TOKEN}' -H 'Content-Type: application/json -d {"name": ${NAME} }`


### Status

* **URI** : `/status`
* **METHODS** : `GET`
* **SUCCESS RESPONSE**
    * **CODE**: 200
    * **TEXT**: `{"msg": "Ok"}`
* **FAILURE RESPONSE**
    * **CODE**: 500
    * **TEXT**: `{"error": "Database is not active"}`  
* **SAMPLE CALL**  
`curl ${SERVER}/status`
