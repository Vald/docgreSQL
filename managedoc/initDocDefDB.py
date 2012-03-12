#! /bin/bash
# encoding: utf-8

# definition of doc_fields TABLE
# it corresponds to available fields in documentation and their args
sqlite3 docDefDB.db "DROP TABLE IF EXISTS doc_fields"
sqlite3 docDefDB.db "CREATE TABLE doc_fields (field TEXT, arg TEXT, PRIMARY KEY (field, arg))"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('title', 'value')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('name', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('name', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('depends', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('depends', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('inheritsFields', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('inheritsFields', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('field', 'name')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('field', 'type')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('field', 'description')"
