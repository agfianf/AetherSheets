import argparse
import sys

import structlog

from services.company_summary import CompanyResearchSummarization

logger = structlog.get_logger(__name__)


def main(
    spreadsheet_id: str,
    input_column: str = "Company Name",
    input_worksheet: str = "Sheet1",
    output_worksheet: str = "Summary",
):
    """Main function to run company research workflow."""

    # Setup logging
    logger.info(
        "Starting company research workflow",
        spreadsheet_id=spreadsheet_id,
        input_worksheet=input_worksheet,
        input_column=input_column,
        output_worksheet=output_worksheet,
    )

    try:
        company_search = CompanyResearchSummarization(spreadsheet_id=spreadsheet_id)
        company_search.run(
            input_column_name=input_column,
            worksheet_input=input_worksheet,
            worksheet_output=output_worksheet,
        )
        logger.info("Company research completed successfully!")

    except Exception as e:
        logger.error("Failed to complete company research", error=str(e), exc_info=True)
        raise


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="AI-powered company research tool that reads company names from Google Sheets and generates summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with spreadsheet ID
  python src/main.py 1Jz_FgPhoU5cfWR_vgNIAFrhJu5quipcWVtiM4G6y5fM

  # Custom worksheets and column names
  python src/main.py <spreadsheet_id> --input-worksheet "Companies" --input-column "Name" --output-worksheet "Research"
        """,
    )

    parser.add_argument(
        "spreadsheet_id", help="Google Sheets spreadsheet ID (found in the URL)"
    )

    parser.add_argument(
        "--input-column",
        default="Company Name",
        help="Name of the column containing company names (default: 'Company Name')",
    )

    parser.add_argument(
        "--input-worksheet",
        default="Sheet1",
        help="Name of the input worksheet (default: 'Sheet1')",
    )

    parser.add_argument(
        "--output-worksheet",
        default="Summary",
        help="Name of the output worksheet (default: 'Summary')",
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    try:
        main(
            spreadsheet_id=args.spreadsheet_id,
            input_column=args.input_column,
            input_worksheet=args.input_worksheet,
            output_worksheet=args.output_worksheet,
        )
    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
