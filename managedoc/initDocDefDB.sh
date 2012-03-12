#! /bin/bash
# encoding: utf-8

# definition of doc_fields TABLE
# it corresponds to available fields in documentation
sqlite3 docDefDB.db "DROP TABLE IF EXISTS doc_fields"
sqlite3 docDefDB.db "CREATE TABLE doc_fields (field TEXT, several TEXT NOT NULL, PRIMARY KEY (field))"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('title', 'False')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('description', 'False')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('name', 'False')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('depends', 'True')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('inheritsFields', 'True')"
sqlite3 docDefDB.db "INSERT INTO doc_fields VALUES ('field', 'True')"
# definition of doc_fields TABLE
# it corresponds to available args for each field in documentation
sqlite3 docDefDB.db "DROP TABLE IF EXISTS doc_field_args"
sqlite3 docDefDB.db "CREATE TABLE doc_field_args (field TEXT REFERENCES doc_fields (field), arg TEXT, PRIMARY KEY (field, arg))"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('title', 'value')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('description', 'value')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('name', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('name', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('depends', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('depends', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('inheritsFields', 'schema')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('inheritsFields', 'table')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('field', 'name')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('field', 'type')"
sqlite3 docDefDB.db "INSERT INTO doc_field_args VALUES ('field', 'description')"
