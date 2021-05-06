## Market Research: Sports Fans in the U.S. and England

### Riley Robertson

</br></br>

## Overview and Background


The most popular sports leagues in each of their respective countries, the National Football League (NFL) and the English Premier League (EPL) have earned the largest sports fan-bases in North America and Europe (and even fans around the globe), making them prime targets for advertising.

One retailer hoping to capitalize on these advertizing goldmines is **OverArmor** - a midsize sports apparel company with locations in the US and England. Although they've been successful enough to matain locations in both countries, they haven't gained the kind of noteriety or traction that would make them a big name brand in either market. They're looking to completely overhaul their marketing strategies for each audience - new ads, sponsorships, social media content, community engagement, and a full rebrand (espeically for their logo... they **desperately** need to hire a real graphic designer).  

</br>

<div style='text-align:center'>
<img src='https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/other_assets/over_armor_logo.png' width='200'>
</div>

</br></br>

## Problem Statement


As part of their overhauled marketing plan, OverArmor has asked me to begin studying the vernacular of both communities via the subreddits: r/nfl and r/PremiereLeague. With a greater understanding of each fanbase's linguistic patterns and colloquialisms, they plan to strategically craft their marketing language to communicate more effectively to their audience. Their specific requests were to collect data, classify posts, and provide insights.

1.  Collect data from each league’s respective Reddit community to build a clean database for investigating the colloquial language used by each fan-base

2. Based on that data, create a machine learning model that can accurately classify a post if the source is unknown

3. Provide insight into the vernacular of each fanbase by creating lists of the most used and most significant words to each community



</br>

## Data Collection

[Notebook 01](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/code/01-Data_Collection.ipynb)

I began with Data collection - in which I ultimately collected 100,000 posts for each subreddit. 

This meant I would have to do a lot of cleaning, but I’d have plenty of options in that process and not have to worry about trying to salvage incomplete or low quality reddit posts. 



</br>

## Data Cleaning

[Notebook 02](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/code/02-Cleaning.ipynb)

My cleaning process brought my total 200k posts down to just 12,000, with a 56/44 % split, making for very balanced classes.

That 56% figure served as baseline model that I would aim to beat. I expexted to be successfull based on the knowledge that there are a lot of easy tells in language used in the context of two very different sports (names of teams, cities, players, coaches, not to mention all of the sport specific vocabulary).

Having finished collecting and cleaning the DataFrame, I had what I needed for the next two phases and also fulfilled the first of OverArmor’s three requests.


</br>

## Data Analysis

[Notebook 03](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/code/03-EDA.ipynb)

In my Data Analysis, I wanted to look at the most common words based on both a straight count of occurrences throughout the data, but also their relative frequency rates.

In this bar chart, we’re looking at the 25 cumulatively most common words - and we see many we might expect the leagues to share in spite of their differences. With only some exceptions like nfl, qb, super, and premier. But for the most part, we see words like season, team, league, players, etc, and of course: football. There's still a lot more valuable information to be gained here, especially if we dig deeper beyond the top 25.

So I provided OverArmor a merged list of the top 200 words from each subreddit that can be used for further analysis to get beyond these most obvious words.





</br>

## Modeling

[Notebook 04](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/code/04-PreProcessing_and_Modeling.ipynb)

With the goal in mind of understanding the language of these two communities, I chose to start with a logistic regression model. Because it’s coefficients can be exponentiated and interpreted, it would serve as a good first model from which I knew I could pull meaningful insights about each word’s impact on the likelihood of a post's classification.

I then moved to a Random Forest model, which would also be able to provide me with insights into individual words being used in the model through feature importances - a measure of relevance between each word and the model.

Because OverArmor asked for modesl that, above all, would be able to make correct predictions, I decided to use Accuracy as my evaluation metric. Both models performed extremely well and will be well suited to classify posts going forward and fulfils OverArmors 2nd request.



</br>

## Conclusions

In accordance with the three objectives given to me by OverArmor, I completed the three following tasks:

1. Collected and cleaned data | Link: [Clean Data Folder](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/data/2_clean)

2. 2 models that could predict posts’ origin subreddit with high accuracy | Link: [Modeling Notebook](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/code/04-PreProcessing_and_Modeling.ipynb)

3. Provided lists of words that could give them insight for marketing decisions | Link: [Data Output Folder](https://git.generalassemb.ly/rileyrobertson/project_3/blob/main/data/3_output)

Additionally, I noticed that many  of the highest ranking words were focused on specific teams, players, and coaches. So I recommended that they look to those sub communities as a way to focus their efforts towards teams and people of greatest interest to their market.

</br>

## With more time: 

- Dive much deeper into the language
- Look at frequency of 2 and 3 word strings (bi-grams/tri-grams)
- Investigate misidentified posts
- Run further testing on posts my models haven’t seen







<!---
Project Structure

Part 1: Data wrangling/gathering/acquisition

Part 2: Cleaning and preprocessing for NLP

Part 3: Classification Modeling 

--->
