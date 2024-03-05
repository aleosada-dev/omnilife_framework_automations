class NotionFilterBuilder:
    def __init__(self):
        self.filter_group = {"and": []}  # Default group
        self.current_group = self.filter_group["and"]
        self.selected_columns = []

    def start_or_group(self):
        """
        Starts a new 'or' condition group.
        """
        or_group = {"or": []}
        self.current_group.append(or_group)
        self.current_group = or_group["or"]
        return self

    def start_and_group(self):
        """
        Starts a new 'and' condition group.
        """
        and_group = {"and": []}
        self.current_group.append(and_group)
        self.current_group = and_group["and"]
        return self

    def end_group(self):
        """
        Ends the current group and returns to the top-level 'and' group.
        """
        self.current_group = self.filter_group["and"]

    def text_filter(self, column_name, condition, value):
        self.current_group.append({"property": column_name, "text": {condition: value}})
        return self

    def richtext_filter(self, column_name, condition, value):
        self.current_group.append(
            {"property": column_name, "rich_text": {condition: value}}
        )
        return self

    def number_filter(self, column_name, condition, value):
        self.current_group.append(
            {"property": column_name, "number": {condition: value}}
        )
        return self

    def datetime_filter(self, column_name, condition, value):
        self.current_group.append({"property": column_name, "date": {condition: value}})
        return self

    def checkbox_filter(self, column_name, condition, value: bool):
        self.current_group.append(
            {"property": column_name, "checkbox": {condition: value}}
        )
        return self

    def build(self):
        """
        Returns the constructed filter object and selected columns.
        """
        return {"filter": self.filter_group}


class NotionSortBuilder:
    def __init__(self):
        self.sorts = {"sorts": []}

    def add_sort(self, column_name, direction="ascending"):
        """
        Adds a sorting instruction for a column.

        :param column_name: Name of the column (property) to sort by.
        :param direction: Direction of the sort, either "ascending" or "descending".
        """
        if direction not in ["ascending", "descending"]:
            raise ValueError("Direction must be either 'ascending' or 'descending'")

        self.sorts["sorts"].append({"property": column_name, "direction": direction})
        return self

    def build(self):
        """
        Returns the constructed sort instructions.
        """
        return self.sorts
