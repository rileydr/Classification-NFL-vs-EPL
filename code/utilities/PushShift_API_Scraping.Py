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