# Vehicular

I like to ride motorcycles (Dualsports, to be specific) and it's well known that the 
best place to look for a good deal on used bikes is craigslist.  In order to jump on
a deal, you've got to constantly troll craigslist for new posts.  

However, I like to automate things when I can, so I wrote this little CLI app to 
search for me.  It uses [feedparser](https://github.com/kurtmckee/feedparser) to 
sort through craigslist rss feeds and sends you an email notification when it finds
new matches.

# Usage

Vehicular runs in a custom shell that manages all the various search parameters.
There are a lot of possible search parameters, inside the shell run `help` to view 
all the commands. and `help <command>` to view help info for `<command>`.  Tab
autocomplete works for commands that have specific options.  Using it is encouraged as
incorrectly typed parameters will fail as invalid.
  
 Of all the parameters, only a few are required: `city`, `seller_type`,
`vehicle_type` and `make_model`.

* `city`
    * Run `city help` to view all available cities in which to search.  
    Tab autocomplete is your friend with this one.
    
* `seller_type`
    * Defaults to search for results from both dealers and owners
    * Run `seller_type dealer` or `seller_type owner` to change it to your desired 
    option
    
* `vehicle_type`
    * Craigslist splits vehicle listings up into motorcycles and cars/trucks
    * run `vehicle_type motorcyle` or `vehicle_type cars/trucks` to select 
    which search you want to run.
    
* `make_model`
    * Selects the make / model you're looking for.  Pretty obvious once you think
    about it.
    
All the other parameters are optional.

After having selected the parameters, run `add_search`, which compiles the selected options into
an RSS URL, which is stored in the database.  After having added the search, running 
`run_search` will parse the searches and send an email notification if matches are found.

# Installation

Install via `pip install vehicular`

# License

GPLv3, see LICENSE.txt

