###### Notes to self:

"""
# Points to make before pseudo-code:
    # what is API? a server that stores information in a format that is easily searchable/accessible to coders
    # what is a request? timing of requests
    # what is a function? simple text based computer program with very specific set of instructions of things to do
    # what is a function input
    # what is a function output
    # function structure - meaning of indents

    #explain display output

    # function anatomy - use screenshot of sample function and sample output


# Possible changes to code

    # Make optional input argument for search parameters (accepts dictionary) 
    # rather than specifying each individual parameter

    # Possibly add arg for custom list of features in output

    # Add Docstring info

"""

###### Pseudo-code draft for Blog post:

"""

# Name function and set input variables including:
# the number of requests to make, the window of time in days for each request, and a list of subreddits
# Anyone using the function can customize how they want to use the code

    # 1


    # 2


    # 3
    # Begin a loop based on the provided list of subreddits
    # This process just says: do the following steps for each subreddit in the list given to the function
    # Everything indented below this loop will be executed  

        # Create an empty list for error/event logging. As the code runs, updates will be added to this list
        # and at the end, the contents of will be saved as a text file so we have a log of every update in the list

        # 3-A
        # Display a status update confirming that scraping for this subreddit is beginning,
        # including subreddit name and current time
        
        # 3-B
        # Add the update from step 3A to the event log list created in step 2
        
        # 3-C
        # Create list of search filters to use in data requests from the API. 
        # These have default settings but can be changed if the user of the function desires to do so
        
        
        # 3-D
        # create an empty list to store data retreived by each request to the API
        
        # 3-C
        # Begin a loop based on the numbers provided as input to the function:
        # The number of requests to make (N) and the window of time in days for each request (D)
        # the code will move backward in time [N] times by increments of [D]
        # Just like the loop we began in step 3, all of the steps indented below 3C are included in this loop

            # 3-C-a          
            # Try/Except to handle any errors in the get_requests
            # Make request for data from current subreddit (based on loop in step 3) 
            # using the information in the list from step 1 and filters in step 3C
    
            # 3-C-a - ERROR
            # If error occured during 3-C-a, add that to the event/error log 
            # with current time and name of the kind of error
            # and display the information in live output for reference
            # (note to self: make sure vocab is uniform for output)
            # then return to step 3-C-a to try the next next request


            # Adding newly pulled data to list for eventual DataFrame conversion and export
            list_data.extend(new_data)
    
            # Adding completion updates to event log
            cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report.append({'event': f'Request complete: {i}',
                           'datetime': f'{cur_datetime}',
                           'exception': ''
                           })
            
            # Onscreen updates for every 10 requests to provide timing updates
            if i % 5 == 0:
                print(f'Request complete: {i}')
                print(f'    Current time: {cur_datetime}')
                print('')
            df_report = pd.DataFrame(report)
            df_report.to_csv(f'../git_ignore/output/report.csv', index=False)
            time.sleep(.25)


        
        # Each request has more information per post than we need, so next the function
        # creates a list of the specific info to keep for each subreddit post
        # title, body text, date/time created, # of comments, etc.

        # creating DataFrame from list after all requests have been made and
        # filters out all information except for the list of features specified in 
        df_output = pd.DataFrame(list_data)
        df_output = df_output[features]
        
        # creating simple date and time columns using utc code
        # https://docs.python.org/3/library/datetime.html#date-objects
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        df_output['date'] = df_output['created_utc'].map(lambda x: dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        df_output['time'] = df_output['created_utc'].map(lambda x: dt.datetime.fromtimestamp(x).strftime('%H:%M:%S'))

        # Exporting primary data output with selected/filtered features
        df_output.reset_index(inplace=True)
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_output.to_csv(f'../git_ignore/output/{cur_datetime}_data_{sub}.csv', index=False,)

        # Exporting secondary output with all features
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_outputfull.to_csv(f'../git_ignore/output/{cur_datetime}_datafull_{sub}.csv', index=False,)
        
        # Exporting event log as a CSV report
        cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.append({'event': f'r/{sub} data files saved to output folder', 'datetime': f'{cur_datetime}'})
        df_report = pd.DataFrame(report)
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_report.to_csv(f'../git_ignore/output/{cur_datetime}_report_{sub}.csv', index=False,)
        report = []

        # Onscreen display - completion of each subreddit scrape
        cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'r/{sub} data and report files saved to output folder')
        print(f'   Current time: {cur_datetime}')
        print('')

"""

###### Full text of Function (check notebook 1 for updates): 

"""

# Function to make [n] requests of 100 posts. 
# Each request will be for a period of [win] days and the periods will not overlap
# Exports .csv of API responses for each subreddit

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def get_nrequest(n, win, subs_list, request_type='submission',
                 size=100, is_self=True, is_video=False):

    # Setting up list of features to retrieve from subreddit data:
    features = ['subreddit', 'created_utc', 'author', 'num_comments', 
                'score', 'is_self', 'link_flair_text','title', 'selftext', 'full_link']

    # List instantiation for error/event logging
    report = []

    # For Loop to scrape multiple subreddits:
    for sub in subs_list:
        
        # Onscreen display during loops:        
        cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'API request initiated. Scraping r/{sub} in progress...')
        print(f'   Current time: {cur_datetime}')
        print('')
        
        # Adding updates to event log
        report.append({'event': f'API request from r/{sub} began',
                       'datetime': f'{cur_datetime}',
                       'exception': ''
                       })

        # Setting parameters to use in data requests from the API. Parameters mostly set by function args. 
        params = {
            'subreddit': sub,
            'size': size,
            'is_self': is_self,
            'is_video': is_video,
            'selftext:not': '[removed]'      # thanks to Amanda for posting this in the groupwork channel
        }

        list_data = []
        
        for i in range(1, n+1):               # I used the demo notebook to figure out these time
            params['after'] = f'{i * win}d'   # parameters and loop structure using n and day_window

            # Try/Except to handle any errors in the get_requests
            try:
                new_data = get_request(params, request_type)

            # Adding errors to event log if get_request fails
            except Exception as e:                                              
                cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report.append({'event': f'REQUEST FAILED: {i}',
                               'datetime': f'{cur_datetime}',
                               'exception': f'{e}'
                               })
                
                # Onscreen display - Failure of single request
                print(f'Request failed: {i}')
                print(f'  Current time: {cur_datetime}')
                print('')
                time.sleep(.25)
                continue
                
            # Adding newly pulled data to list for eventual DataFrame conversion and export
            list_data.extend(new_data)
    
            # Adding completion updates to event log
            cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report.append({'event': f'Request complete: {i}',
                           'datetime': f'{cur_datetime}',
                           'exception': ''
                           })
            
            # Onscreen updates for every 10 requests to provide timing updates
            if i % 5 == 0:
                print(f'Request complete: {i}')
                print(f'    Current time: {cur_datetime}')
                print('')
            df_report = pd.DataFrame(report)
            df_report.to_csv(f'../git_ignore/output/report.csv', index=False)
            time.sleep(.25)

        # creating DataFrame from list after all requests have been made    
        df_output = pd.DataFrame(list_data)
        df_outputfull = pd.DataFrame(list_data)
        
        df_output = df_output[features]
        
        # creating simple date and time columns using utc code
        # https://docs.python.org/3/library/datetime.html#date-objects
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        df_output['date'] = df_output['created_utc'].map(lambda x: dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        df_output['time'] = df_output['created_utc'].map(lambda x: dt.datetime.fromtimestamp(x).strftime('%H:%M:%S'))

        # Exporting primary data output with selected/filtered features
        df_output.reset_index(inplace=True)
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_output.to_csv(f'../git_ignore/output/{cur_datetime}_data_{sub}.csv', index=False,)

        # Exporting secondary output with all features
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_outputfull.to_csv(f'../git_ignore/output/{cur_datetime}_datafull_{sub}.csv', index=False,)
        
        # Exporting event log as a CSV report
        cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.append({'event': f'r/{sub} data files saved to output folder', 'datetime': f'{cur_datetime}'})
        df_report = pd.DataFrame(report)
        cur_datetime = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        df_report.to_csv(f'../git_ignore/output/{cur_datetime}_report_{sub}.csv', index=False,)
        report = []

        # Onscreen display - completion of each subreddit scrape
        cur_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'r/{sub} data and report files saved to output folder')
        print(f'   Current time: {cur_datetime}')
        print('')


"""