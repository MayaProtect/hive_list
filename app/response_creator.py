from pymongo.cursor import Cursor

from app.hive import Hive


class ResponseCreator:
    def __init__(self, response: Cursor | list, total_count: int, page: int, page_size: int):
        """
        Create a response creator
        :param response:
        :param total_count:
        :param page:
        :param page_size:
        """
        if response is None:
            raise ValueError("The response must not be None")

        if type(response) is not Cursor and type(response) is not list:
            raise TypeError("The response must be a Cursor or a list")

        if total_count is None:
            raise ValueError("The total_count must not be None")

        if type(total_count) is not int:
            raise TypeError("The total_count must be an int")

        if page is None:
            raise ValueError("The page must not be None")

        if type(page) is not int:
            raise TypeError("The page must be an int")

        if page_size is None:
            raise ValueError("The page_size must not be None")

        if type(page_size) is not int:
            raise TypeError("The page_size must be an int")

        self.total_count = total_count
        self.page = page
        self.page_size = page_size
        self.response = response
        self.hives = []
        for hive in response:
            try:
                self.hives.append(Hive(hive))
            except Exception as e:
                print(e)

    def create_response(self) -> dict:
        """
        Create response
        :return:
        """
        hives = []
        for hive in self.hives:
            hives.append(hive.__to_json__())
        response = {
            "count_hives": self.total_count,
            "actual_page": self.page,
            "elements_per_page": self.page_size,
            "hives": hives
        }

        return response
