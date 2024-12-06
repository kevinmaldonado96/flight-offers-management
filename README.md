# flight-offers-management

the project flight-offers-management is conformed by multiple microservices, each one represents a different business unit, such as flight management, offers publication, luggage management, etc, likewise we have microservices which represent different microservices patterns such as aggregators, orchestrators, etc. Additionally we have specific functions of google cloud platform which perform asynchronous processes, sending emails, etc.

Below you will find more details on the structure of the project:

* **.github:** in this folder you will find everything related to the project's continuous integration, scripts with actions
* **kubernates:** in this folder you will find the kubernates configuration files such as pod deployment specifications, services, ingress creation and mapping, and secrets configuration.
* **gcp-funcions**:
  * in this folder you will find the gcp functions, which through a topic publish and subscribe to obtain information and process it, in addition to this they send emails.
  * **technologies:** python, sengrid, google-cloud-pubsub
* **msusers:**
  * microservice that is in charge of storing the application users, in addition to this, it is in charge of authentication.
  * **technologies:** kotlin, docker, postgresql, springmock
* **offers:**
  * microservices publishing flight and baggage offers.
  * **technologies:** python, flask, sqlalchemy, pytest
* **post:**
  * microservices publishing flight and baggage post.
  * **technologies:** python, flask, sqlalchemy, pytest
* **score:**
  * microservice that measures user's score.
  * **technologies:** python, flask, sqlalchemy, pytest
* **route:**
  * microservice that manages the routes of the registered flights.
  * **technologies:** python, flask, sqlalchemy, pytest
* **rf003:**
  * orchestrated microservice, which allows you to create a post, create a path, perform rollback of previous posts in case one of them fails.
  * **technologies:** python, flask, flask-restfull, pytest, request
* **rf005:**
  * orchestrated microservice, which allows you to create a post, create a path, perform rollback of previous posts in case one of them fails.
  * **technologies:** python, flask, flask-restfull, pytest, request
* **rf04:**
  * microservice orchestrator which is in charge of bidding on a previously created post.
  * **technologies:** kotlin, docker, springmock
* **dodcker-compose:** file which allows the application to be deployed locally in docker
 
    
  
