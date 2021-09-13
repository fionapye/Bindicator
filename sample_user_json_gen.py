#user weburl and pushover tokens config

import os
import json
import platform


# paths between platforms
if platform.system() == 'Windows':
    wdir = 'D:\\GitHub\\Bindicator'
elif platform.system() == 'Linux':
    wdir = '/home/pi/Documents/Bindicator'

# make a folder called user_config and ENSURE this is in the gitignore
#   DO NOT COMMIT YOUR USER DATA TO GITHUB!
os.chdir(os.path.join(wdir,'user_config'))


def write_json (filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# add your data here
users = {
    "<user1>" : {"council" : "<add_council_as_in_xpaths>"
        ,"urlpath" : "<add_house_bin_collection_url>"
        , "apptoken" : "<add_bindicator_pushover_app_token>"
        , "usertoken" : "<add_user_pushover_token>"
        },
    "[user2]" : {"council" : "<add_council_as_in_xpaths>"
        ,"urlpath" : "<add_house_bin_collection_url>"
        , "apptoken" : "<add_bindicator_pushover_app_token>"
        , "usertoken" : "<add_user_pushover_token>"
        }
}


write_json('users.json', users)
