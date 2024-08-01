#this is actually probably not going to work
#it's too easy to overwrite, if I'm trying to store quite a bit of data over time
#probably a sqlite database would be better
#wow this is getting way more complicated than I thought it would
#I guess that's the difference between a one-time thing (which isn't really possible thanks to rate limiting) 
#thanks ao3 hackers

#would a json for the unique IDs help?
#json can't store objects
#and an object alone can't be used to match to a unique ID
#so use a json as a linking tool?
#json holds all user IDs and work IDs?
#pickle (for now) holds all loaded objects?
#and export to csv or google sheet for actual processing?


import pickle
import os

folder_name = "Data_Sources"
pickle_path = os.path.join(folder_name, "author_last_reload.pickle")
userpicklepath = os.path.join(folder_name, "users.pickle")
workpicklepath = os.path.join(folder_name, "works.pickle")

def update_pickle_file(existing_data, new_user, new_work, pickle_file):
    # Update or append new user object
    existing_user_ids = [user['User ID'] for user in existing_data['Users']]
    if new_user['User ID'] in existing_user_ids:
        # Update existing user object
        existing_data['Users'] = [user if user['User ID'] != new_user['User ID'] else new_user for user in existing_data['Users']]
    else:
        # Append new user object
        existing_data['Users'].append(new_user)

    # Update or append new work object
    existing_work_ids = [work['Work ID'] for work in existing_data['Works']]
    if new_work['Work ID'] in existing_work_ids:
        # Update existing work object
        existing_data['Works'] = [work if work['Work ID'] != new_work['Work ID'] else new_work for work in existing_data['Works']]
    else:
        # Append new work object
        existing_data['Works'].append(new_work)

    # Serialize and save the updated data structure to the pickle file
    with open(pickle_file, 'wb') as file:
        pickle.dump(existing_data, file)

def gather_user_info(users):
    loaded_user_info = []

    # Assuming instances of MyClass are stored somewhere accessible
    for user in loaded_authors:
        instance_info = {
            'User': user,
            'Username': str(user.username),
            'User ID': int(user.user_id) or None, #only loaded after refresh, and can only be loaded with an authenticated session
            'last reload date': datetime.today()
        }
        loaded_user_info.append(instance_info)

    return loaded_user_info

def gather_work_info(works):
    loaded_works_info = []

    # Assuming instances of MyClass are stored somewhere accessible
    for work in loaded_works:
        instance_info = {
            'Work': work,
            'Work ID': int(work.id), #this is a class attribute that is loaded with the initial load
            'Fandoms': list(work.fandoms), #this is a class attribute that only exists after reload
            'last reload date': datetime.today()
        }
        loaded_works_info.append(instance_info)

    return loaded_works_info
    

#old code, delete later, this is for posterity because I haven't worked out how to do it with the new data structure yet
def load_author_last_reload(pickle_path):
    try:
        with open(pickle_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def save_author_last_reload(author_last_reload, pickle_path):
    with open(pickle_path, 'wb') as file:
        pickle.dump(author_last_reload, file)