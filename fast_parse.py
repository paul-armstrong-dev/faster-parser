from concurrent import futures
from loguru import logger
import pandas as pd


def fast_parse(python_class, parse_function, data_to_parse, number_of_workers=4, **kwargs):
    """
        Util function to split any data set to the number of workers,
        Then return results using any give parsing function

        Note that when using dicts the Index of the Key will be passed to the function
        Object too, so that needs to be handled
    :param python_class: Instantiated class object which contains the parse function
    :param parse_function: Function to parse data, can either be list or dict
    :param data_to_parse: Data to be parsed
    :param number_of_workers: Number of workers to split the parsing to
    :param kwargs: Optional, extra params which parse function may need
    :return:
    """
    try:
        function_object = getattr(python_class, parse_function)
    except AttributeError as e:
        logger.error(f"{python_class} doesn't have {parse_function}")
        return
    else:
        results = []
        with futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
            if type(data_to_parse)==list:
                future_to_result = {executor.submit(function_object, data, **kwargs): data for data in data_to_parse}
            elif type(data_to_parse)==dict or type(data_to_parse)==pd.Series:
                for index, data in data_to_parse.items():
                    future_to_result = {executor.submit(function_object, index, data, **kwargs)}
            else:
                logger.error("Unsupported data type")
                return
            for future in futures.as_completed(future_to_result):
                try:
                    data = future.result()
                except Exception as exc:
                    logger.error(f"{future_to_result[future]} generated an exception: {exc}")
                else:
                    results.append(data)
        return results
