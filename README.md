# Stock Watch Project

Project to send an SMS whenever certain price indicators are met for any stock on the stock market. 

The project will wait for the market to open and then create threads that continously poll for the price of stocks on a single server only. The project uses Twilio to send text messages.

I expanded this project to run fully distributed using kubernetes. There is now an API node that partitions stock symbols to worker nodes who collect data. The API portion is available here: [Implied Volatility API](https://github.com/mateoreyrosa/IVApi) 
