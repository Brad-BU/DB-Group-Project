# DB-Group-Project
Team Name: 2B || !2B

Team Members:
- Brad Buckingham
- Bryce Clark
- Josh Wilson
- William Ding

Admin Username/Password:
- Username: admin
- Password: password1234

Set up and start venv (mac): \
python3 -m venv venv \
source venv/bin/activate

Required Python Packages:
pip install flask \
pip install flask-sqlalchemy \
pip install flask-migrate \
pip install flask-wtf \
pip install flask-login \
pip install email-validator

# What we Did
After installing all packages above, we modfied the baseball database by running the following commands.


GRANT ALL PRIVILEGES ON *.* TO 'web'@localhost;

create table User( \
id int primary key auto_increment, \ 
username varchar(64) not null unique key, \
email varchar(64) not null unique key, \
password_hash varchar(128) not null \
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
