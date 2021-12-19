CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, nickname TEXT, password TEXT);
CREATE TABLE households (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE access (householdid INTEGER, userid INTEGER, admin BOOLEAN DEFAULT FALSE);
CREATE TABLE tasks (id SERIAL PRIMARY KEY, householdid INTEGER, name TEXT, description TEXT, deadline DATE, complete BOOLEAN DEFAULT FALSE);
CREATE TABLE assignees (taskID INTEGER, userID INTEGER);

