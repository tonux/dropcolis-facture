# Facture Generator

A Python script to automatically generate facture (invoice) PDFs from HTML templates and send them to Directus via the `/import` endpoint.

## Features

- **API Integration**: Retrieves facture data from Dropcolis API
- **PDF Generation**: Creates professional PDFs from HTML templates using WeasyPrint
- **Directus Upload**: Automatically uploads generated PDFs to Directus
- **Tax Calculation**: Automatically calculates Canadian TPS (5%) and TVQ (9.975%) taxes
- **Error Handling**: Comprehensive logging and error handling
- **Template System**: Uses Jinja2 templating for flexible HTML generation

## Prerequisites

- Python 3.8 or higher
- System dependencies for WeasyPrint (see installation section)

### System Dependencies (macOS)

```bash
# Install system dependencies using Homebrew
brew install cairo pango gdk-pixbuf libffi
```

### System Dependencies (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

### System Dependencies (CentOS/RHEL)

```bash
# Install system dependencies
sudo yum install gcc libffi-devel python3-devel python3-pip cairo pango gdk-pixbuf2
```

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   - Edit `config.json` with your actual API endpoints and tokens
   - Ensure the HTML template path is correct

## Configuration

Edit `config.json` with your actual values:

```json
{
  "dropcolis_api_url": "https://services.dropcolis.ca",
  "directus_api_url": "https://your-directus-instance.com",
  "directus_token": "your-actual-directus-token",
  "template_path": "facture_template.html"
}
```

### Configuration Fields

- **dropcolis_api_url**: Base URL for the Dropcolis API
- **directus_api_url**: Base URL for your Directus instance
- **directus_token**: Bearer token for Directus authentication
- **template_path**: Path to the HTML template file

## Usage

### Basic Usage

```bash
python generate_facture.py
```

### Running as a Service

You can set up the script to run automatically:

```bash
# Add to crontab to run every hour
0 * * * * cd /path/to/project && python generate_facture.py >> /var/log/facture_generator.log 2>&1
```

## How It Works

1. **Data Retrieval**: Fetches facture data from `https://services.dropcolis.ca/items/Factures?fields=*.*`
2. **PDF Generation**: For each facture, renders the HTML template with data and generates a PDF
3. **Directus Upload**: Uploads each PDF to Directus with metadata
4. **Cleanup**: Removes temporary files and logs results

## HTML Template

The HTML template (`facture_template.html`) uses Jinja2 syntax and includes:

- Company branding and contact information
- Client details and invoice information
- Billing table with items and totals
- Automatic tax calculations (TPS and TVQ)
- Payment conditions and signature line

### Template Variables

The template expects the following variables:

- `facture_number`: Invoice ID from the API
- `date`: Invoice emission date (`date_emission`)
- `date_service`: Service date (`date_service`)
- `client_id`: Client UUID from client object
- `client_name`: Client first name from client object
- `client_location`: Client location from client object
- `items`: Array of billing lines (`lignes`)
- `subtotal`: Subtotal before taxes (calculated from items)
- `tps`: TPS tax amount (calculated)
- `tvq`: TVQ tax amount (calculated)
- `grand_total`: Total including taxes (calculated)

## API Response Format

The script expects the Dropcolis API to return data in this format:

```json
{
  "data": [
    {
      "id": "facture_id",
      "status": "A_PAYER",
      "montant": 100,
      "montant_ttc": 100,
      "devise": "CAD",
      "mode_paiement": "Interact",
      "date_service": "2025-08-31T12:00:00",
      "date_emission": "2025-08-23T12:00:00",
      "client": {
        "id": "client_uuid",
        "first_name": "Client Name",
        "location": "Client Location"
      },
      "lignes": [
        {
          "id": 1,
          "facture": 1,
          "prix_unitaire": 10,
          "quantite": 3,
          "frais": 20,
          "total": 100
        }
      ]
    }
  ]
}
```

## Directus Integration

The script uploads PDFs to Directus using the `/files` endpoint with:

- File metadata (title, description, collection)
- Facture ID and client information
- Generation timestamp
- Proper file naming convention

## Logging

The script provides comprehensive logging:

- INFO level for successful operations
- ERROR level for failures
- WARNING level for configuration issues
- All logs include timestamps and context

## Error Handling

The script handles various error scenarios:

- API connection failures
- Invalid data formats
- PDF generation errors
- Directus upload failures
- Configuration issues

## Troubleshooting

### Common Issues

1. **WeasyPrint Installation Errors**
   - Ensure system dependencies are installed
   - Try reinstalling with: `pip uninstall weasyprint && pip install weasyprint`

2. **API Connection Issues**
   - Verify API URLs in config.json
   - Check network connectivity
   - Validate API tokens

3. **PDF Generation Failures**
   - Check HTML template syntax
   - Verify template file path
   - Ensure sufficient disk space

4. **Directus Upload Errors**
   - Verify Directus token and permissions
   - Check Directus API endpoint
   - Ensure collection exists in Directus

### Debug Mode

To enable debug logging, modify the logging level in the script:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Customization

### Adding New Fields

To add new fields to the invoice:

1. Update the HTML template with new variables
2. Modify the `generate_pdf` method to include new data
3. Update the API response handling if needed

### Modifying Tax Calculations

Tax rates are defined in the `calculate_taxes` method:

```python
def calculate_taxes(self, subtotal: float) -> tuple:
    tps_rate = 0.05      # 5% TPS
    tvq_rate = 0.09975   # 9.975% TVQ
    # ... rest of method
```

### Custom HTML Templates

You can create multiple HTML templates and switch between them by:

1. Creating new template files
2. Updating the template_path in config.json
3. Or modifying the script to support multiple templates

## Security Considerations

- Store API tokens securely
- Use HTTPS for all API communications
- Implement proper access controls
- Regularly rotate authentication tokens
- Monitor API usage and logs

## Performance

- The script processes factures sequentially to avoid overwhelming APIs
- Temporary PDF files are automatically cleaned up
- Memory usage is optimized for large numbers of factures
- Timeout settings prevent hanging on slow API responses

## Support

For issues and questions:

1. Check the logs for error messages
2. Verify configuration settings
3. Test API endpoints manually
4. Review system dependencies

## License

This project is provided as-is for internal use. Please ensure compliance with your organization's policies and applicable regulations.
