First create a new folder.
Open that folder in VS code or any other IDE
Then, copy the repository link
In vs code, go to new terminal.
Then do the following:
  git clone "Repo Link"
  cd './stockpredictionfinal./'
  python -m venv venv    (Create a new virtual environment)
  venv\Scripts\Activate  (Activate the virtual environment)
  pip install -r requirements/txt   (Install the required packages)
  cd './back./'
  python manage.py runserver 
  Then click on the link shown

  Well done!, now you are going to predict the price of your stocks.
  
