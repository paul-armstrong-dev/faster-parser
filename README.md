# faster-parser
Quick and dirty API speedup for lists of data

### Faster python API's in two minutes; really just one line of code to change

(My favourite utility function that I have written since coming into python)

----
#### Problem
In my last job I was tasked with recreating the data models which were coming out of a few social & subscription
data API's (YouTube being a good example), and was frankly hugely disappointed with the performance of Python
when downloading these files using requests and pd.to_csv to create the files.

YouTube data was downloading in 10-15 minutes when processing 450MB's of data. As the process was pretty lightweight in production
this wasn't any real problem, but in test, needing to repeatedly downloading the files, this became **infuriating**.
----
This is a very common problem with API's and python, and I have looked into the externally available solutions from
[Dask](https://dask.org/); [Ray](https://ray.readthedocs.io/en/latest/); [Modin](https://github.com/modin-project/modin)
and some more task specific options like [AsyncIO](https://docs.python.org/3/library/asyncio.html)

But found each of these had some pretty frustrating issues: requiring pretty big rewrites, not supporting certain environments and having huge
dependency lists & overhead.

---
A golden rule in multithreading/multiprocessing is that you really shouldn't implement it unless you **absolutely** need to because of
 the amount of headaches it can cause for a tiny bit of extra performance in some functions. All of the above solutions
 confirmed this, with some test implementations failing for unknown reasons and swallowing my NAS's CPU power for an entire night.

The problem I was having really didn't seem to merit such extreme solutions, so I sought to simplify, I looked back into
 the concurrency options provide by the python built in **Concurrent and Futures** libraries, and have been hugely impressed.

While the actual concurrency engine will never perform as well as the externals I mentioned earlier the simplicity of
 implementation is pretty much unbeatable, and seemed to bring day to day concurrency back into the realm of normality in python.

After reading up on the built in classes I implemented the below in 30 minutes over a lunch break, (and have now
implemented it in another 10 API's just to be sure.) and would like to share/discuss the code and possible improvements and next steps.

Basically, its a static utility function which accepts an instantiated class (as an object), and a function to use to
process data (as a string), and then a list of the  data which you would like to parse. I named the function **fast_parse**
 as it should theoretically work with absolutely any type of function which you would like to process data with.

I added **kwargs as an optional param (incase there are any which are passed through all functions), and a number of workers
so that when deploying across environments we are able to configure the functions to operate depending on the server.

I'm really surprised there aren't more concurrency functions which have been structured in this way, after implementing
this the run times of the downloads went from 10-15 minutes to consistently 2-3 minutes, the only change which was required
in the processing class was the import and then:
```python
    processed_data = get_youtube_data(unprocessed_data)
    """becomes"""
    processed_data=utils.fast_parse(self, "get_youtube_data", unprocessed_data)
```
---
(Loguru is the one external library included, if you don't use it already I suggest you do (especially for multithreading),
there is a great wrapper from them which allows catching the errors across all the threads while also only needing to change line of code)

#### TL;DR

In the repo there is a function which you can copy paste as is and it should make your functions faster.
See example usage above :P

#### Implementation notes
- If you don't need/want to handle pd.Series in your implemented I would recommend removing pandas completely
as it does come with quite a big overhead in terms of requirements


#### Example pip usage
```
pip install faster-parser
```

```
from faster_parser import faster_parse

processed_data = get_youtube_data(unprocessed_data)
"""becomes"""
processed_data=utils.fast_parse(self, "get_youtube_data", unprocessed_data)
```
