# CSI 3335 DB Group Project: Team Info
Team Name: Baseball \
BA - Baylor \
S - Software \
E - Engineering \
B - Buddies \
A - And \
L - Living \
L - Legends

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

create table teamsupd as select * from teams; \
create table battingupd as select * from batting; \
create table pitchingupd as select * from pitching;

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
- Added user support to the database. With a user name, email, and encrypted password.
- An SQL program to create the user table(s)
- Web/database app that requires users to login into the system.
- Once logged in, the user may provide a team name and a year via drop down menu requesting the team name, and then a drop down menu with the valid years. The system will log the selections made by a user.
- A web page to display the standings for the division for the team and year submitted. If the submitted team made the playoffs, additional information regarding the playoffs should be included.
- An admin user (password should be included in your readme file). The admin user can see the logged information for each user and the totals for all users.

# Extra Credit
Create a new user function \
Dynamic dropdown boxes \
Remember me check box at login
