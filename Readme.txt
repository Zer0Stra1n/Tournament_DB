Note: This Readme assumes you are using the basic vagrant install required by the class.

To run this project, simply to the following:
  1) Clone this folder into the vagrant subfolder within the fullstack folder provided by the class (fullstack/vagrant)

  2) After you vagrant up and vagrant ssh, navigate to this folder within the vagrant sub-folder

  3) Access the psql command line by typing psql

  4) Type the following:
        Create database tournament;

  5) Type the following to access the newly created database:
        \c tournament

  6) Type the following to import the tournament.sql file.
        \i tournament.sql

  7) Control+D out of the psql console

  8) Type the following to run all of the tests
        python tournament_test.py
