import structlog

from graphs.company_research import create_graph_company_summary
from integrations.sheet import GoogleSheetsClient

logger = structlog.get_logger(__name__)


class CompanyResearchSummarization:
    def __init__(self, spreadsheet_id: str | None = None):
        logger.debug(
            "Initializing CompanyResearchSummarization",
            spreadsheet_id=spreadsheet_id,
        )

        self.graph = create_graph_company_summary()
        self.sheet = GoogleSheetsClient(spreadsheet_id=spreadsheet_id)

    def run(
        self,
        worksheet_input: str,
        input_column_name: str = "Company Name",
        worksheet_output: str = "Review Company",
    ):
        logger.info(
            "Starting company research run",
            worksheet_input=worksheet_input,
            input_column_name=input_column_name,
            worksheet_output=worksheet_output,
        )

        # Get all companies listed
        sheet_data = self.sheet.read_cell(worksheet_name=worksheet_input)
        companies = [
            data[input_column_name]
            for data in sheet_data
            if data.get(input_column_name)
        ]

        logger.info(
            "Found companies to process",
            count=len(companies),
            companies=companies,
        )

        for i, company_name in enumerate(companies, 1):
            logger.info(
                "Processing company",
                company=company_name,
                progress=f"{i}/{len(companies)}",
            )

            try:
                result = self.graph.invoke({"company": company_name})
                final_summary = result["final_summary"]

                self.sheet.append_rows(
                    columns=["Company", "Summary"],
                    values=[[company_name, final_summary]],
                    worksheet_name=worksheet_output,
                )

                logger.info(
                    "Completed company research",
                    company=company_name,
                    summary_length=len(final_summary),
                )

            except Exception as e:
                logger.error(
                    "Failed to process company",
                    company=company_name,
                    error=str(e),
                    exc_info=True,
                )
                # Continue with next company rather than failing entire batch
                continue


if __name__ == "__main__":
    research = CompanyResearchSummarization(
        spreadsheet_id="1Jz_FgPhoU5cfWR_vgNIAFrhJu5quipcWVtiM4G6y5fM"
    )
    research.run(
        input_column_name="Company Name",
        worksheet_input="Sheet1",
        worksheet_output="Summary",
    )
