# Housework manager

Tietokantasovellus-kurssin harjoitustyö


Application for managing and sharing housework tasks. Registered users can have access to Household(s), which hold Housework Task(s). These tasks (e.g. "Clean bathroom", "Grocery shopping") each hold one or more attributes.

Application is available [here](https://tsoha-housework-manager.herokuapp.com/).

There are two test users: tester / password and user / MYpassword

The "beef" of the application is in _routes.py_, which handles requests, using modules _users.py_, _households.py_ and _tasks.py_. Html-files are found under _templates_, and they utilize _layout.html_.

The functionality of the application:

- User can log in and out and create a new user 
- User has a username (unique) and nickname shown in the application (not unique)
- User can delete their account 
- User can change their nickname
- After logging in, the user will see the household(s) they have access to 
- Household has a name and can hold housework tasks in a household they have access to
- User can see in a household the names of users that have access to that household 
- User can create a new household, that initially only they have access to. They become the household admin 
- Household admin can give other users access or admin rights to the household based on username 
- Household admin can remove users from the household 
- User can remove themself from a household they have access to
- User can view, modify and add housework 
- Housework tasks include attributes: name, description, deadline, user(s) assigned to, completed
- Task attributes can be empty 
- User can assign themself to housework tasks 
- Housework tasks can be marked completed
- Tasks can be deleted
- Number of contributing users/admins in a household is not limited

Points for improvement/continuing development:

- Application will get into an error state if not logged in user tries to see My Households page, or if logged in user tries to see a household page they don't have access to. This is not pretty, but hey, it works.
- _routes.py_ has gotten so big it could be refactored. Other refactorings might also be a good idea.
- Code styling should be improved according to Python practices
- Current version has no error messages for the user. 
