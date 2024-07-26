# What is the software application?
Login to the NPR system, downloads donation reports for some period of time, and queries in those reports when a donation was made for a specified Business (through the Business' EIN)

# Who's it intended for
For anyone that needs to know when a ticket of a specific Business was donated (generally the last time)

# What problem does the software solves?
The difficult process of login with an user in the NPR system, manually querying and downloading the donation report and search through the report for the specified Business EIN (in the ticket's Access Key)

# How is it going to work?
By automatizing every step of the manual process:
* Login in the NPR System with an account
* Download the donation report for a specific month (or period)
* Searching through the report for the specified Business EIN in the Access Key

# What are the main concepts that are involved and how are they related?
* Authentication and Login:
  * The software needs to handle user authentication and login to the online service.
  * Concepts include user credentials, authentication protocols (OAuth, SAML), and session management.

* File Download:
  * After successful login, the software must download relevant files associated with the account.
  * Concepts include HTTP/HTTPS requests, file retrieval, and data transfer.

* Data Analysis:
  * The downloaded files need analysis. This involves extracting meaningful information.
  * Concepts include data parsing, data transformation, and data visualization.

* Security and Compliance:
  * Ensuring data security and compliance with standards (e.g., GDPR, HIPAA) is crucial.
  * Concepts include encryption, access controls, and audit logs.