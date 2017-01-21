CONTENTS OF THE FILE
--------------------

* About Sync assignment
*

# About sync assignment
 ----------------------
 database creation : database creation is a file,which creates a database required for the assignment.
 filewatcher : in this file filewatcher keeps watch on target directory which takes argument as target directory.
 compressor : in this file compressor compresses the file and keeps in database(tempdb.tgz.md5).
 validator :validates the json file and keeps the content in database(tempdb-json) 
   - json_content_validator : which checks a json valid file or not.
       - allvalidationfun: this file validates the content of the json file.
 xml parsing: this is sub file parses a config.xml files to fetch time and path.

