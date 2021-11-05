# Housework manager

Tietokantasovellus-kurssin harjoitustyö


I will create an application for managing and sharing housework tasks. Registered users can have access to Household(s), which hold Housework Task(s). These tasks (e.g. "Clean bathroom", "Grocery shopping") each hold one or more attributes.


Application features:


- User can log in and out and create a new user
- User has a username (unique) and name shown in the application (not unique)
- User can delete their account
- After logging in, the user will see the household(s) they have access to
- Household has a name and can hold housework tasks
- User can see in a household the names of users that have access to that household 
- User can create a new household, that initially only they have access to. They become the household admin
- Household admin can give other users access or admin rights to the household based on username
- Household admin can remove users from the household
- User can remove themself from a household they have access to
- User can view, modify and add housework tasks under a household they have access to
- Housework tasks include attributes: name, description, estimated time to complete, deadline, user(s) assigned to.
- Task attributes can be empty
- User can create custom task attributes
- User can assign themself to housework tasks 
- Household admin can assign other users to tasks
- Housework tasks can be marked hidden or unavailable for certain users, who are not household admins. (for example, to filter out tasks that a kid can't do from their view)
- Number of contributing users/admins in a household is not limited
- In household view, tasks can be arranged and filtered based on their attributes
- Housework tasks can be made recurring
- Housework tasks can be copied to make a base for a new task
- User cannot see tasks from households they don't have access to. User cannot see households they don't have access to. Anyone not logged in cannot see any tasks or households.

