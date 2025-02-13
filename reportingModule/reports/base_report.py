from abc import ABC, abstractmethod
import pandas as pd

class BaseReport(ABC):
    def __init__(self, fields, filters, user=None):
        """
        :param fields: List of fields/columns the user wants in the report.
        :param filters: Dictionary of filters (e.g., date range, status, etc.).
        :param user: The current user (for permission or user-specific queries).
        """
        self.fields = fields
        self.filters = filters
        self.user = user

    @abstractmethod
    def get_data(self):
        """
        Must be implemented by subclasses to fetch data based on the filters.
        Returns a list of dictionaries or any structure that can be transformed into a DataFrame.
        """
        pass

    def format_data(self, data):
        """
        Formats data as a pandas DataFrame and selects only the requested fields.
        """
        df = pd.DataFrame(data)
        if self.fields:
            # Ensure we only include valid columns (assuming the data contains them)
            df = df[[col for col in self.fields if col in df.columns]]
        return df

    def generate(self, export_format='csv'):
        """
        Fetch, format, and export the report in the desired format.
        """
        data = self.get_data()
        df = self.format_data(data)
        
        if export_format == 'csv':
            return df.to_csv(index=False)
        elif export_format == 'excel':
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()
        else:
            raise ValueError("Unsupported export format")