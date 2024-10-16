SYSTEM = f"""
You are a useful assistant that can categorize Reddit posts according to if they are likely to exhibit market sentiment from investors in the comments.
The comment unlikely to exhibit sentiment are 'Rate my portfolio' type comments, need for portfolio advices, Hypothetical scenarios like 'What if the market turned down by 20%', Theoritical questions like 'Why would someone exercise an option prior to expiration rather than sell it?', or general questions that don't involve any stocks like 'How do you make a choice between two companies, one with better returns and one with better margins?'. On the contrary, these are comments likely to exhibit market sentiment in the comment: 'Nvidia reports 122% revenue growth on surging demand for data center chips', 'CHWY earnings beat the catalyst to set off the pet industry stocks comeback. WOOF maybe next?', 'Trump Media stock falls below $20 per share, a first since company went public', also asking thoughts about stocks like :'I have been looking at this two stocks for a little bit. I know EPD comes with the K-1 tax form.\n\nOverall, what do you think of these two. Both pay nice dividends and seem to be growing nicely. \n\nI know that energy can be risky but it seems like EPD is growing. \n\nSEVN is a little tricky because the housing rates are tough. \n\nOverall, any advice and thoughts are appreciated!'"""

FILTER_PROMPT = f"""
Given the title and the body of a reddit post, you will tell if the post is likely to exhibit sentiment from people that respond to it in the comments.
You will output your answer in one word only 'YES' or 'NO'.
Here are some examples:

Title: "Apple stock hits an all-time high amid strong iPhone sales."
Body: "Apple's shares are up 3% today, reaching a new all-time high as the company reports robust iPhone sales in the latest quarter."
Answer: YES

Title: "Rate my portfolio: AAPL, MSFT, TSLA, and AMZN"
Body: "Looking for feedback on my portfolio. I'm 80% in tech stocks, with AAPL, MSFT, TSLA, and AMZN making up the bulk. Thoughts?"
Answer: NO

Title: "Tesla's latest delivery numbers fall short of Wall Street expectations."
Body: "Tesla delivered 241,300 vehicles in Q3, falling short of the 250,000 vehicles analysts expected. How will this impact the stock?"
Answer: YES

Title: "What would happen if the Fed suddenly raised interest rates by 2%?"
Body: "Just curious about the potential impacts on the market if the Federal Reserve unexpectedly increased interest rates by 2%. How would stocks and bonds react?"
Answer: NO

Title: "Amazon faces antitrust scrutiny over its dominance in online retail."
Body: "The FTC is reportedly investigating Amazon's practices for possible antitrust violations. Could this lead to a breakup of the company?"
Answer: YES

Title: "Why is the P/E ratio important when evaluating stocks?"
Body: "I've heard a lot about the P/E ratio being a key metric in stock analysis, but why exactly is it so significant? How should I interpret it?"
Answer: NO

Title: "Disney stock falls after disappointing theme park revenue."
Body: "Disney's latest earnings report shows weaker-than-expected revenue from its theme parks, sending shares down 4% in after-hours trading."
Answer: YES

Title: "How do you diversify your portfolio in a volatile market?"
Body: "I'm new to investing and am trying to understand the best ways to diversify my portfolio, especially during times of market volatility."
Answer: NO

Title: "Nvidia's new AI chip outperforms competition, stock surges 5%."
Body: "Nvidia's latest AI chip is setting new benchmarks in performance, pushing the stock up 5% in today's trading session."
Answer: YES

Title: "What’s the difference between a market order and a limit order?"
Body: "I’m trying to understand the basics of stock trading. Can someone explain the difference between a market order and a limit order?"
Answer: NO

Title: "Netflix shares drop as subscriber growth slows."
Body: "Netflix reported slower subscriber growth in its latest earnings report, causing shares to drop by 6% in after-hours trading."
Answer: YES

Title: "How would a recession impact the housing market?"
Body: "Just wondering, if we enter a recession, how might that affect the housing market? Are there any historical examples?"
Answer: NO

Title: "Google's ad revenue takes a hit amid increased competition."
Body: "Google's latest earnings report shows a decline in ad revenue, attributed to growing competition from other tech giants."
Answer: YES

Title: "What are the tax implications of investing in REITs?"
Body: "I'm considering investing in Real Estate Investment Trusts (REITs). Can anyone explain the tax implications?"
Answer: NO

Title: "Microsoft announces acquisition of AI startup, shares rise."
Body: "Microsoft has announced the acquisition of a leading AI startup, boosting investor confidence and pushing shares up by 4%."
Answer: YES

Title: "Is it better to invest in index funds or individual stocks?"
Body: "I'm trying to decide between investing in index funds or picking individual stocks. What are the pros and cons of each?"
Answer: NO

Title: "Facebook faces backlash over privacy concerns, stock dips."
Body: "Facebook's stock is down 2% today following reports of a new privacy scandal. How will this affect the company's future?"
Answer: YES

Title: "What are the key factors that drive stock prices up or down?"
Body: "I'm trying to understand what causes stock prices to fluctuate. What are the most important factors?"
Answer: NO

Title: "Robinhood stock plunges after quarterly earnings miss."
Body: "Robinhood shares are down 7% after the company reported lower-than-expected earnings for the quarter."
Answer: YES

Title: "If the market went down 20% what stock would be your choice to pickup on a discount?"
Body: "I'm in my early 30s and starting to think seriously about retirement. What stocks do you recommend for long-term planning?"
Answer: NO

Title: "Meta announces layoffs as part of cost-cutting measures, stock rises."
Body: "Meta is laying off 10% of its workforce to cut costs, and the stock has responded positively, rising 3% today."
Answer: YES

Title: "How do interest rates affect bond prices?"
Body: "Can someone explain how changes in interest rates impact bond prices? I'm new to bond investing and trying to learn the basics."
Answer: NO

Title: "AMC stock surges as 'Barbenheimer' becomes a blockbuster hit."
Body: "AMC shares are up 12% today as the 'Barbenheimer' movie trend brings record-breaking box office numbers."
Answer: YES

Title: "What’s the best way to rebalance a portfolio?"
Body: "I hold\n\nADBE- $500\n\nAMD- $7000\n\nAVGO- $15,000\n\nNVDA- $32,000\n\nFSELX- $15,000\n\nFSPTX- $9,000\n\nFXAIX- $115,000\n\nFZILX- $100\n\nMKTAY- $900\n\nMU- $400\n\nAmeritas acct- $12,000 but no access until October\n\nCash- $45,000\n\nHYSA- $20,000\n\nMy portfolio is 3 years old. Up ~$40k, mostly on FXAIX and FSELX. I\u2019m 36M. Thinking about selling AMD & AVGO and going NVDA, FSELX or FXAIX with the funds.f"
Answer: NO

Title: "GameStop stock jumps on speculation of a potential acquisition."
Body: "Rumors are swirling that GameStop may be acquired by a larger company, and the stock has jumped 8% today in response."
Answer: YES

Title: "How does inflation affect my purchasing power?"
Body: "I'm trying to understand how inflation impacts my money over time. Can someone explain the concept of purchasing power?"
Answer: NO

Title: "Tesla faces recall of 500,000 vehicles over safety concerns, shares drop."
Body: "Tesla's stock is down 5% today following news that the company is recalling 500,000 vehicles due to potential safety issues."
Answer: YES

Title: "What are your thoughts on dividend investing?"
Body: "I'm considering focusing more on dividend-paying stocks in my portfolio. Do you think this is a good strategy for long-term growth?"
Answer: NO

Title: "Snapchat's user growth stalls, stock plummets 15%."
Body: "Snapchat reported that user growth has stalled in its latest earnings report, causing the stock to drop sharply."
Answer: YES

Title: "How do you decide when to sell a stock?"
Body: "I’m curious about how experienced investors decide when it’s time to sell a stock. What factors do you consider?"
Answer: NO

Now give the Answer for the following post:
"""

def build_prompt(title:str, body:str):
    prompt = FILTER_PROMPT + f"Title: {title}\nBody: {body}"
    return prompt

def build_system_prompt():
    return SYSTEM

# if __name__ == '__main__':
#     print(build_prompt('a', 'b'))