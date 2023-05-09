# TransactionAlgorithmWithSygus

For this project, I wanted to create transaction algorithm usig sygus, and run it on python. 
The goal of transaction algorithm is to determine when to buy or sell stocks based on historical data. 
There are a lot of data on stock available in websites such as https://finance.yahoo.com/quote/QQQ/history?p=QQQ, and I decided to use history of closing price to determine a good time to buy or sell.

## Example algorithm

One simple algorithm I wanted to implement waw Moving Average Crossover Strategy (MACD). Moving average refers to average price of a stock for a given period of time. For instance, 20 day moving average would be average of the prices over the past 20 trading days. 

There are 3 components to this algorithm:

1. Short term moving average
2. Long term moving average
3. The crossover

Two moving averages are calculated. Then, comparing those two, when the shorter term moving average crosses above the longer term moving average, it suggests that it is a good time to buy, since there is an upward trend. 
Conversely, when the longer term moving average crosses above the shorter term moving average, it suggests that it is a good time to sell, since there is a downward trend.

## Implementation - .sy file
In order to create this algorithm with sygus, I tried to define 2 main functions- one to calculate the moving average given an array and total days, and another to compare two given moving averages to determine whether to buy or sell.
This is where I spend the most of the times, as I kept facing errors, with all z3, cvc4 and yice solvers. Since the solvers do not provide a detailed debug message, it was a lot of trial and errors: sygus files start with a set-logic such as (set-logic LIA). It was hard to figure out one that supports all Reals, Array, and Integer, while fixing syntax errors of the sygus file.
After trying different combinations of function declarations with set-logics such as AUFLIA, QF_LRA, UF, UFLRA..etc, I found one that solves my .sy file.


## Implementation - .py file
Then, using python, I imported the sy file , defined the function, create model, and tried to run it with a dummy data. What took the most time on this step is figuring out what functions to use for the imprted z3. For instance: 
After converting .sy file with:  parsed_sygus = z3.parse_smt2_file("sygusInput.sy") it took me a while to figure out the "parsed_sygus" variable is in form of array: 

[ForAll([prices, days],
        mov-avg(prices, days) ==
        If(days == 0,
           ToReal(0),
           prices[days + 1 - days]/ToReal(days) +
           (ToReal(days - 1)/ToReal(days))*
           mov-avg(prices, days - 1))),
 ForAll([shortma, longma, threshold],
        compare-ma(shortma, longma, threshold) ==
        If(shortma > longma + threshold, 1, 0))] 
        
According to documentation it was supposed to convet it to a z3.ExprRef object, but it was not the case. 

Then, I ran in to issues trying to let the function run with the model: 

mov_avg_value = model.evaluate(mov_avg(prices_array, z3.IntVal(days)))
compare_ma_value = model.evaluate(compare_ma(z3.RealVal(shortma), z3.RealVal(longma), z3.RealVal(threshold)))
print("mov_avg:", mov_avg_value)
print("compare_ma:", compare_ma_value)

I was expecting the code above to return the result of the function defined in .sy file, but it returned these instead: 

mov_avg: mov_avg(Store(Store(Store(Store(Store(Store(Store(Store(Store(Store(Store(prices,
                                        0,
                                        100),
                                        1,
                                        101),
                                        2,
                                        120),
                                        3,
                                        130),
                                        4,
                                        104),
                                        5,
                                        150),
                                      6,
                                      106),
                                7,
                                107),
                          8,
                          180),
                    9,
                    120),
              10,
              100),
        5)
compare_ma: compare_ma(4, 6, 2)

Instead of numerical value, it returned expressinos of the functions. After some research I found that model.evaluate()  returns symbolic expressions, and they need to be converted to numbers.
This is where I could not proceed further, as I could not find appropriate methods to do so. The error messages included "ArithRef' object has no attribute '...' " where '...' were converstion methods I tried to find.

I came to conclusion that there could be issues either in my .sy file, the parse from the .sy file using z3, or the way I create solver , model and the function. Since the .sy file does not return any error when I run them on terminal, I am guessing that it is the latter.

## Conclusion

I wanted to implement multiple transaction algorithms and actually run them with past stock data, but due to the issues I faced, I did not get a chance to do so.
I am glad I got to have more hands on experience with sygus, but I realized that it takes much longer to write and run something and make it work. If I get a chance to figure out what is causing the issue in my code, I would like to finish it up, try implementing more algorithms and compare their efficiency.
