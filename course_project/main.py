import utils
import sys
from getpass import getpass

con, cursor = utils.create_connection()

first_level_functions = {
    0: 'Register',
    1: 'Log in'

}

all_functions = {
    0: 'Add new records (admin)',
    1: 'Actions with records (select, update, delete) and custom queries (admin)',
    2: 'Search records by name',
    3: 'Find albums by the name and release date',
    4: 'Find albums by the release date',
    5: 'Artists of the label',
    6: 'Artists of the country',
    7: 'Find artist-album-track',
    100: 'Help',
    400: 'Exit'
}

print_help = {
    'Search records by name': "This option helps you to find any record in the music library \n",
    'Find albums by the name and release date': "This option helps you to find THE ALBUM that you are looking for using"
                                                " name and release date to make no mistakes \n",
    'Find albums by the release date': "This option helps you to find all albums between entered dates \n",
    'Artists of the label': "This option helps you to find everything about artist-label collaborations using record "
                            "label name and dates of partnership \n",
    'Artists of the country': "This option helps you to find every artist of the country that you entered \n",
    'Find artist-album-track': "This option helps you to find every artist/album/track and everything connected with "
                               "it \n",
    'Exit': "This option helps you to get out of this little library-program",

}


def session(user):
    while True:
        print('Menu')
        for action_fun in all_functions:
            print('{} : {}'.format(action_fun, all_functions[action_fun]))
        session_action = None
        while session_action is None:
            try:
                print('\nEnter the action: ', end='')
                session_action = int(input())
            except ValueError:
                session_action = None
                print('You entered wrong value, try again')

        try:
            if session_action == 0:
                if user.admin is True:
                    utils.adding_records_to_tables(cursor)
                else:
                    print('You have got no permission to perform this action')
            elif session_action == 1:
                if user.admin is True:
                    utils.action_with_records(cursor)
                else:
                    print('You have got no permission to perform this action')
            elif session_action == 2:
                print('Who or what do you want to find?')
                find_actions = ['album', 'singer', 'genre', 'record label', 'track']

                print('Available tables: ', find_actions)
                find_action = input()
                while find_action not in find_actions:
                    print('Please, try again')
                    print('Available tables: ', find_actions)
                    find_action = input()

                print('Name: ', end='')
                find_name = input()
                utils.find_records_by_name(cursor, find_name, find_action)
            elif session_action == 3:
                print('What album do you want to find?')
                print('Name: ', end='')
                album_name = input()
                print('Release date (YYYY-MM-DD): ', end='')
                album_release_date = input()
                utils.find_record_by_name_release_date(cursor, album_name, album_release_date)
            elif session_action == 4:
                print('What from-release-date of album do you want to find (YYYY-MM-DD)?')
                from_date = input()
                print('What to-release-date of album do you want to find (YYYY-MM-DD or nothing)?')
                to_date = input()
                utils.find_albums_by_release_date(cursor, from_date, to_date)
            elif session_action == 5:
                print('What record label are you looking for?')
                label_name = input()
                print('What from-collab-date of collaboration with record label do you want to find (YYYY-MM-DD)?')
                from_date = input()
                print('What to-collab-date of collaboration with record label do you want to find (YYYY-MM-DD)?')
                to_date = input()
                utils.record_label_partnership(cursor, label_name, from_date, to_date)
            elif session_action == 6:
                print('What country are interested in?')
                country_name = input()
                utils.find_singers_by_country(cursor, country_name)
            elif session_action == 7:
                print('What do you want to find? [singer, album, track]')
                option = input()
                print('Enter the name: ', end='')
                name = input()
                utils.find_singer_album_track(cursor, name, option[0])
            elif session_action == 100:
                for item in print_help:
                    print(item, end='\t --> \t')
                    print(print_help[item])
            elif session_action == 400:
                print('Goodbye!')
                sys.exit(0)
            else:
                print('Wrong menu item. Try again')

        except (ValueError, KeyError) as err:
            print('Please, try again: {}'.format(err))


def login():
    result = False
    while not result:
        print('Username: ', end='')
        username = input()
        password = getpass()

        try:
            user_obj = utils.check_user(cursor, username, password)
            result = True
        except (ValueError, KeyError):
            print('Log in failed. Try to log in again')
            result = False
    session(user_obj)


def registration():
    print('Welcome to the registration form! Please, enter your username)')
    print('Username: ', end='')

    username = input()
    while len(username) > 100:
        print('Your username is too long, try to use less characters')
        print('Username: ', end='')

        username = input()

    print('Password: ', end='')
    password = getpass()
    try:
        utils.registration(con, cursor, (username, password, False))
    except EnvironmentError:
        print('Registration failed.')


if __name__ == '__main__':
    print('Welcome to musical library database client!')
    print('Menu')
    for a in first_level_functions:
        print('{} : {}'.format(a, first_level_functions[a]))
    action = None
    while action is None:
        try:
            print('\nEnter the action: ', end='')
            action = int(input())
        except ValueError:
            action = None
            print('You entered wrong value, try again')

    if action == 0:
        registration()
    elif action == 1:
        login()
