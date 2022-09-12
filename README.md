# khmerasr

This project using flask framwork to built the entire website of Khmer ASR to record the voice from spaeker and manage those data.
To run khmerasr project:

  # to install all python packages that use in this particular project.
  1st: run pip install -r requirements.txt 
  
  # to install all packages in node that use in this particular project.
  2nd: run npm install
  
  # to run database migration (sqlite)
  3rd: run python migration.py
  
  # to run seeder to store dummy data in database
  4th: run python seeders.py
  
  # to run the project
  5th: run python run.py
  
  # In order to save the time you can run step 3, 4, 5 together by using command below in your terminal
  ./runscrip.sh
