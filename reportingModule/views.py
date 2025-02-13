# reportingModule/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .reports.report_factory import ReportFactory

class GenerateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Expected JSON payload:
        {
            "report_type": "sales",         # or 'vaccination', 'animal', etc.
            "fields": ["id", "amount", ...],  # list of fields the user wants
            "filters": {"start_date": "2025-01-01", "end_date": "2025-01-31"},
            "export_format": "csv"            # or 'excel'
        }
        """
        data = request.data
        report_type = data.get('report_type')
        fields = data.get('fields', [])
        filters = data.get('filters', {})
        export_format = data.get('export_format', 'csv')
        
        try:
            # Use the factory to create the proper report instance.
            report = ReportFactory.create_report(report_type, fields, filters, user=request.user)
            output = report.generate(export_format=export_format)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # For binary data (like Excel), you might want to return a FileResponse.
        # Here we simply return the content as a string for demonstration.
        return Response({"report": output})
