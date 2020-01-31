# PCBot
PCBot for discord servers. Price checks for Path of Exile (POE) using the POE trade api

There are two versions of this bot.  
One version is designed to interact with a StressTestBot which will input a series of PC requests in semi rapid succession and both bots will keep track of response time.  StressTestBot can also be used tcreate a queue of price checks that you may want repeatedly over a period of time.  If you are planning to use this version, then you should also download the StressTestBot files and make necessary adjustments to bot ID.

The other version of the bot is pure vanilla and does not interact with anything other than the Discord API.  If you are cloning the bot, you will need to create your own Discord app and generate your own bot token

Future plans for this bot include changing the way the data is processed, but runtime differences will most likely be negligible due to small size of data.  There are plans to better organize the async features of this bot and make them "smarter" as currently it is not the most efficient.
