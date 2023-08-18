# Contents of this repository

## Calorie Crave Project
- Project for Modul: Entwicklung von Web-Anwendungen
- Prof: Alexander Eck
- Students: Linus Widing, Justin Grünberg and Michael Otieno

## Executing the app
1. set up and activate a [Python Virtual Environment](https://hwrberlin.github.io/fswd/01-python-vscode.html#32-use-the-python-virtual-environment-as-default-for-this-workspace).
2. install the required Python packages from the terminal with the command `pip install -r requirements.txt`:
3. start the web server via ` gunicorn -w 4 -b 0.0.0.0:8000 app:app`
4. go to your browser and open [http://0.0.0.0:8000/](http://0.0.0.0:8000/)
5. you can now sign in or up and use the app to your desire

**Creating demo recipes**

- Database can be populated with demo recipes to get a better understanding of what the app will look and feel like. 
- To do so go to the route : `/populate-db`
- You can now go back to the home page and reload the page.

## Using the app
- The app is designed to be als intuitive as possible 
- You can use the navbar to navigate to all important pages
- On the home-page itself you can filter recipes using the form on the left
- Clicking the title of a recipe will lead you to further details
- When creating a new recipe the recipe itself should be described on the left and Ingredients can be added on the right side of the page
- To add a recipe to your favorites simply click the heart on the right of a recipe
- If you want to view your favorite recipes simply turn on the 'Show favorites' filter and press filter
- 