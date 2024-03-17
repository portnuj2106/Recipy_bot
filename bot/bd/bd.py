import sqlalchemy as db


class UserDatabase:
    def __init__(self, database_uri):
        self.engine = db.create_engine(database_uri)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.users = db.Table("users", self.metadata,
                       db.Column('user_id', db.Integer, primary_key=True),
                             db.Column('user_name', db.TEXT),
                             db.Column('user_email', db.TEXT),
                             db.Column('users_recipes', db.TEXT),
                             )
        self.metadata.create_all(self.engine)

    def add_user(self, user_id, user_name, user_email):
        insert_statement = self.users.insert().values(user_id=user_id, user_name=user_name, user_email=user_email)
        self.connection.execute(insert_statement)
        self.connection.commit()

    def get_all_users(self):
        select_statement = self.users.select()
        result = self.connection.execute(select_statement)
        users = result.fetchall()
        return users

    def get_user_by_id(self, user_id):
        select_statement = self.users.select().where(self.users.columns.user_id == user_id)
        result = self.connection.execute(select_statement)
        user = result.fetchone()
        if user:
            return {
                'user_id': user[0],
                'user_name': user[1],
                'user_email': user[2],
                'users_recipes': user[3]
            }
        else:
            return None

    def user_exists(self, user_id):
        select_statement = self.users.select().where(self.users.columns.user_id == user_id)
        result = self.connection.execute(select_statement)
        return result.fetchone() is not None

    def delete_user(self, user_id):
        delete_statement = self.users.delete().where(self.users.columns.user_id == user_id)
        self.connection.execute(delete_statement)
        self.connection.commit()

    def add_user_recipe(self, user_id, recipe_id):
        user = self.get_user_by_id(user_id)
        existing_recipes = user.get('users_recipes')

        if existing_recipes is None:
            existing_recipes = ''

        updated_recipes = existing_recipes + str(recipe_id) + ','

        update_statement = self.users.update(). \
            where(self.users.columns.user_id == user_id). \
            values(users_recipes=updated_recipes)
        self.connection.execute(update_statement)
        self.connection.commit()

    def is_authorized(self, user_id):
        user = self.get_user_by_id(user_id)
        return user is not None

    def get_user_recipes_string(self, user_id):
        select_statement = self.users.select().where(self.users.columns.user_id == user_id)
        result = self.connection.execute(select_statement)

        user = result.fetchone()
        if user:
            return user[3]
        else:
            return None

    def delete_user_recipe(self, user_id, recipe_id):
        # Retrieve the concatenated string of recipe IDs for the user
        user_recipes_string = self.get_user_recipes_string(user_id)
        if user_recipes_string:
            # Convert the concatenated string to a list of recipe IDs
            user_recipes_list = user_recipes_string.split(',')
            # Remove the specified recipe ID from the list
            if str(recipe_id) in user_recipes_list:
                user_recipes_list.remove(str(recipe_id))
                # Convert the updated list back into a concatenated string
                updated_recipes_string = ','.join(user_recipes_list)
                # Update the database with the modified concatenated string
                update_statement = self.users.update(). \
                    where(self.users.columns.user_id == user_id). \
                    values(users_recipes=updated_recipes_string)
                self.connection.execute(update_statement)
                self.connection.commit()
            else:
                print("Recipe ID not found in user's recipes")
        else:
            print("User not found or user has no recipes")

users_db = UserDatabase('sqlite:///users-sqlalchemy.db')