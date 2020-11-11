# Set up React  
0. `cd ~/environment && git clone https://github.com/NJIT-CS490/musikalee && cd musikalee`    
1. Install your stuff!    
  a) `npm install && npm install -g webpack && npm install --save-dev webpack && npm install socket.io-client --save && sudo pip install requests`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    

# Set up PSQL
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`  
    Enter yes to all prompts.  
2. Initialize PSQL database: `sudo service postgresql initdb`  
3. Start PSQL: `sudo service postgresql start`  
2. Make a new superuser: `sudo -u postgres createuser --superuser $USER`  
    If you get an error saying "could not change directory", that's okay! It worked!
3. Make a new database: `sudo -u postgres createdb $USER`  
        If you get an error saying "could not change directory", that's okay! It worked!
4. Make sure your user shows up:  
    a) `psql`  
    b) `\du` look for ec2-user as a user  
    c) `\l` look for ec2-user as a database  
5. Make a new user:  
    a) `psql` (if you already quit out of psql)  
    b) Type this with a new unique password:  
    `create user some_username_here superuser password 'some_unique_new_password_here';`  
    c) `\q` to quit out of sql  

# Getting PSQL to work with Python
1. Update yum: `sudo yum update`, and enter yes to all prompts  
2. Get psycopg2: `pip install psycopg2-binary`  
3. Get SQLAlchemy: `pip install Flask-SQLAlchemy==2.1`  
4. Get Dot-Env: `pip install python-dotenv`
4. Make a new file called `sql.env` and add `DATABASE_URL='postgresql://{username_here}:{password_here}@localhost/postgres'` in it

# Enabling read/write from SQLAlchemy  
  There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `trust` in Vim: `:%s/ident/trust/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created! 

# Set up your DB    
1. Run `sudo service postgresql start && python`
2. In the python interactive shell, run:
      `import models`
      `models.DB.create_all()`
      `models.DB.session.commit()`

# Set up React Libraries
1. Run `npm install --save react-router-dom && npm install react-spotify-login` 
# Set up React-Router-Dom
1. Run `npm install --save react-router-dom` 

# Set up Spotify Login
npm i react-spotify-login

# Set Up Spotify
1. Navigate to https://developer.spotify.com/dashboard/login and sign up or login <br />
2. Go to your dashboard and create a project (any appropriate title/description is fine) <br />
3. Click on the project to see your Client ID and Client Secret <br />
4. Under your main directory create a file called `spotify.env` and populate it as follows:
```
SPOTIFY_CLIENT_ID={your client id here}
SPOTIFY_CLIENT_SECRET={your client secret here}
```
*\*note the lack of quotes*
<br />
