# reportingModule/reports/report_factory.py

from .sales_report import SalesReport
from .vaccination_report import VaccinationReport
from .animal_report import AnimalReport  # assuming you have this

class ReportFactory:
    @staticmethod
    def create_report(report_type, fields, filters, user=None):
        """
        :param report_type: A string indicating the type of report (e.g., 'sales', 'vaccination', 'animal')
        """
        if report_type == 'sales':
            return SalesReport(fields, filters, user)
        elif report_type == 'vaccination':
            return VaccinationReport(fields, filters, user)
        elif report_type == 'animal':
            return AnimalReport(fields, filters, user)
        else:
            raise ValueError(f"Invalid Report Type: {report_type}")
