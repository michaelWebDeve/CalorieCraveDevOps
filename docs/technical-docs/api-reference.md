---
title: API Reference
parent: Technical Docs
nav_order: 4
---

[Jane Dane]
{: .label }

# [API reference]
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## [Section / module]

### `function_definition()`

**Route:** `/route/`

**Methods:** `POST` `GET` `PATCH` `PUT` `DELETE`

**Purpose:** [Short explanation of what the function does and why]

**Sample output:**

[Show an image, string output, or similar illustration -- or write NONE if function generates no output]

---

##  Login

### `login()`

**Route:** `/login`

**Methods:** `"POST", "GET"`

**Purpose:** Handle login functionality.

**Sample output:**

![login() sample](../assets/images/login.png)



---
##  Registration

### `register()`

**Route:** `/register`

**Methods:** `"POST", "GET"`

**Purpose:** Handle register functionality.

**Sample output:**

![register() sample](../assets/images/register.png)

---
##  Homepage
### `index()`

**Route:** `/`

**Purpose:** Render homepage.

### `function downloadContent(counter, limit, query_str)`

**Route:** `/api/recipes/?counter=`

**Purpose:** Retrieve and display recipes provided parameters and user preferences. It fetches recipe data from an API 
endpoint and dynamically generates HTML elements to display the recipes on the page, including their images, names, 
nutritional information.

### `function toggleFavorite(recipeId, buttonContainer)`

**Route:** `/api/toggle_favorite?user_id=`

**Methods:** `POST`

**Purpose:** Handle the addition and removal of recipes from a user's list of favorite recipes.

**Sample output:**

![index() sample](../assets/images/homepage.png)




---
##  Recipe detail page
### `get_recipe()`

**Route:** `/recipe/<recipe_id>`

**Purpose:** Retrieve recipe with `recipe_id` from database and present it to user.

**Sample output:**

![get_recipe() sample](../assets/images/recipe_detail.png)

---
##  Populate database

### `pop_db()`

**Route:** `/populate-db`


**Purpose:** Flush the database and insert sample data set

**Sample output:**

![populate_db() sample](../assets/images/populateDb.png)

---
## Show own recipes
### xxxxxxxxxxxxxxxxxxx

**Route:** `xxxxxxxxxxxxxxxxxxxxxxxxxx


**Purpose:** xxxxxxxxxxxxxxxxxxxx

**Sample output:**

![populate_db() sample](../assets/images/xxxxxxxxxxx.png)
Browser shows: `Database flushed and populated with some sample data.`

## [app.py]

### `change_email():`

**Route:** `/change_email`

**Methods:** `POST`

**Purpose:** allows a logged-in user to change their email address. It checks if the user is logged in and verifies the current password. If everything is correct, it updates the email address in the database and session, then notifies the user of the successful change.

**Sample output:**
![Change Email](../assets/images/change_email.png)


## [app.py]

### `change_password()`

**Route:** `/change_password`

**Methods:** `POST` 

**Purpose:** allows a logged-in user to change their password. It performs checks to ensure the user is authenticated, the new password and its confirmation match, and the current password is correct. If all validations pass, it updates the user's password in the database.

**Sample output:**
![Change Password](../assets/images/change_password.png)

