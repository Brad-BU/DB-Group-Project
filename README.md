# CSI 3335 DB Group Project: Team Info
Team Name: Baseball

Team Members:
- Brad Buckingham
- Bryce Clark
- Josh Wilson
- William Ding

# Prerequisites
Set up and start venv (mac): \
python3 -m venv venv \
source venv/bin/activate

Required Python Packages:\
pip install flask \
pip install flask-sqlalchemy \
pip install flask-migrate \
pip install flask-wtf \
pip install flask-login \
pip install email-validator

# Changes We Made To The Database
After installing all packages above, we modfied the baseball database by running the following commands.


GRANT ALL PRIVILEGES ON *.* TO 'web'@localhost;

create table User( \
id int primary key auto_increment, \
username varchar(64) not null unique key, \
email varchar(64) not null unique key, \
password_hash varchar(256) not null \
);

create table UserActions( \
id int primary key auto_increment, \
userId int not null, \
username varchar(64) not null, \
search_filter0 varchar(64) not null, \
search_filter1 varchar(64) not null, \
result varchar(64) not null, \
datetime varchar(64) not null \
);

After running the above, we wrote python scripts and ran each to make changes to the data base. All of which are placed in the folder named 'updates'


Our copy of the database is stored in baseball.sql


# Websites Used To Update Database
https://www.baseball-reference.com/leagues/majors/2022.shtml

# Log In Info
Admin Username/Password:
- Username: admin
- Password: password1234


# Programming Languages Used
Python \
HTML \
CSS \
JavaScript

# Minimum Requirements


# Extra Credit
Create a new user function \
Dynamic Dropdown boxes


