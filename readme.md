# Disclaimer:

I, the creator of this code, am in no way, shape or form responsible for any financial losses, misfunctioning of the application, or any other issues related to the use of this.

I do not reccomend using this application with real money, especially if you don't know what you're doing, or you can't affort to lose it.

## Welcome!
Make sure the strategies you are trading are actually profitable by doing realtime backtesting.

### Now here the most important:
In order for this to work, you need a working Tradingview Strategy. Read here, if you don't know what that is:
https://www.tradingview.com/support/solutions/43000562362-what-are-strategies-backtesting-and-forward-testing/

You will need at least a pro+ subscription on tradingView in order to use this bot (the webhook feature is not included in the free account). Get an account here to support my work: https://www.tradingview.com/gopro/?share_your_love=pb-algo

You're going to have to make some adjustments in your strategy scripts. Simply replace the "order id", which is the id your strategy orders get. If you need help with this, get in touch with me on upwork: https://www.upwork.com/freelancers/~01b77066f97bc1eb38

The hook is set up to react to the following order ID's (which are set in the strategies code):
Long, Short, Close Long, Close Short

Examples:

- Entries:
  strategy.entry("Long", strategy.long, when = buySignal) 
  strategy.entry("Short", strategy.short, when = sellSignal)

The OrderID's in the above examples are "Long" and "Short"

- Exits:
  if strategy.position_size > 0
  strategy.exit(id='Long', limit=longTake, stop=longStop)
  if strategy.position_size < 0
  strategy.exit(id='Short', limit=shortTake, stop=shortStop)

The OrderID's in the above examples are "Long" and "Short"



## If you need help with setting this bot up, or want to connect a different exchange, feel free to get in touch with me on upwork:
https://www.upwork.com/freelancers/~01b77066f97bc1eb38
