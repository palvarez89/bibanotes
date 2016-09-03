BibaNotes
=========

Simple Web Service to store comments for [BiBa Android App].

[BiBa Android App]: https://github.com/palvarez89/BiBa-Bicicleta-Publica-Badajoz

Developer docs:
--------------

To forward the ports available in OpenShift:

    rhc port-forward bibanotes

To connect to the database:

    mysql --host=$OPENSHIFT_MYSQL_DB_HOST --user=$OPENSHIFT_MYSQL_DB_USERNAME --password=$OPENSHIFT_MYSQL_DB_PASSWORD
