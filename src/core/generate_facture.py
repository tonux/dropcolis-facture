#!/usr/bin/env python3
"""
Facture Generator Script
Retrieves facture data from Dropcolis API, generates PDFs from HTML templates,
and sends them to Directus via POST /import endpoint.
"""

import requests
import json
import os
import tempfile
import base64
from datetime import datetime, timedelta
from jinja2 import Template
from weasyprint import HTML, CSS
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FactureGenerator:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the FactureGenerator with configuration.
        
        Args:
            config: Configuration dictionary containing API endpoints and settings
        """
        self.config = config
        self.dropcolis_api_url = config['dropcolis_api_url']
        self.directus_api_url = config['directus_api_url']
        self.directus_token = config['directus_token']
        self.template_path = config['template_path']
        
        # Load HTML template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template = Template(f.read())
        
        # Load and encode logo as base64
        self.logo_base64 = self._load_logo_base64()
    
    def _load_logo_base64(self) -> str:
        """
        Load the logo image and convert it to base64 for embedding in HTML.
        
        Returns:
            Base64 encoded image string or empty string if logo not found
        """
        try:
            logo_path = os.path.join(os.path.dirname(self.template_path), 'logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = base64.b64encode(f.read()).decode('utf-8')
                    return f'data:image/png;base64,{logo_data}'
            else:
                logger.warning(f"Logo file not found at {logo_path}")
                return ''
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            return ''
    
    def retrieve_factures(self, id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve facture data from Dropcolis API.
        
        Returns:
            List of facture dictionaries
        """
        try:
            logger.info("Retrieving factures from Dropcolis API...")
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.directus_token}'
            }
            
            if id:
                response = requests.get(
                    f"{self.dropcolis_api_url}/items/Factures?filter[id][_eq]={id}&fields=id,status,montant,montant_ttc,devise,mode_paiement,date_service,date_emission,client.*,lignes.*",
                    headers=headers,
                    timeout=30
                )
            else:
                response = requests.get(
                f"{self.dropcolis_api_url}/items/Factures?filter[status][_eq]=A_PAYER&fields=id,status,montant,montant_ttc,devise,mode_paiement,date_service,date_emission,client.*,lignes.*",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                factures = data.get('data', [])
                logger.info(f"Successfully retrieved {len(factures)} factures")
                return factures
            else:
                logger.error(f"Failed to retrieve factures. Status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving factures: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving factures: {e}")
            return []
    
    def format_date(self, date_string: str) -> str:
        """
        Format date string from ISO format to French format.
        
        Args:
            date_string: Date string in ISO format (e.g., "2025-08-23T12:00:00")
            
        Returns:
            Formatted date string (e.g., "23/08/2025")
        """
        if not date_string or date_string == 'N/A':
            return 'N/A'
        
        try:
            # Parse ISO date string
            if 'T' in date_string:
                # Remove time part if present
                date_part = date_string.split('T')[0]
            else:
                date_part = date_string
            
            # Parse the date
            parsed_date = datetime.strptime(date_part, '%Y-%m-%d')
            
            # Format to French date format
            return parsed_date.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            # If parsing fails, return original string
            return date_string
    
    def calculate_taxes(self, subtotal: float) -> tuple:
        """
        Calculate TPS and TVQ taxes for Canadian invoices.
        
        Args:
            subtotal: Subtotal amount before taxes
            
        Returns:
            Tuple of (tps, tvq, grand_total)
        """
        tps_rate = 0.05  # 5% TPS
        tvq_rate = 0.09975  # 9.975% TVQ
        
        tps = round(subtotal * tps_rate, 2)
        tvq = round(subtotal * tvq_rate, 2)
        grand_total = round(subtotal + tps + tvq, 2)
        
        return tps, tvq, grand_total
    
    def generate_pdf(self, facture_data: Dict[str, Any]) -> Optional[tuple]:
        """
        Generate PDF from HTML template using facture data.
        
        Args:
            facture_data: Dictionary containing facture information
            
        Returns:
            Tuple containing (pdf_path, grand_total, subtotal) or None if failed
        """
        try:
            logger.info(f"Generating PDF for facture {facture_data.get('id', 'unknown')}")
            
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            # Prepare template variables
            template_vars = {
                'current_date': current_date,
                'facture_number': facture_data.get('id', facture_data.get('numero', 'N/A')),
                'date': self.format_date(facture_data.get('date_emission')),
                'date_service': self.format_date(facture_data.get('date_service')),
                'client': facture_data.get('client', {}),
                'items': facture_data.get('lignes', []),
                'subtotal': 0,
                'tps': 0,
                'tvq': 0,
                'grand_total': 0,
                'status': facture_data.get('status', 'N/A'),
                'logo_base64': self.logo_base64
            }
            
            # Calculate totals
            subtotal = 0
            for item in template_vars['items']:
                item_total = (item.get('prix_unitaire', 0) * item.get('quantite', 0)) + item.get('frais', 0)
                item['total'] = item_total
                subtotal += item_total
            
            template_vars['subtotal'] = subtotal
            tps, tvq, grand_total = self.calculate_taxes(subtotal)
            template_vars['tps'] = tps
            template_vars['tvq'] = tvq
            template_vars['grand_total'] = grand_total
            
            # Render HTML template
            html_content = self.template.render(**template_vars)
            
            # Create temporary file for PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                pdf_path = tmp_file.name
            
            # Generate PDF using WeasyPrint
            HTML(string=html_content).write_pdf(pdf_path)
            
            logger.info(f"PDF generated successfully: {pdf_path}")
            return pdf_path, grand_total, subtotal
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return None
    
    def send_to_directus(self, pdf_path: str, facture_data: Dict[str, Any], grand_total: float, subtotal: float) -> bool:
        """
        Send PDF file to Directus via POST /import endpoint.
        
        Args:
            pdf_path: Path to the PDF file
            facture_data: Original facture data for metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Sending PDF to Directus for facture {facture_data.get('id', 'unknown')}")
            current_date = datetime.now().strftime('%Y-%m-%d')
            # Prepare file for upload
            with open(pdf_path, 'rb') as pdf_file:
                files = {
                    'file': (f"facture_{facture_data.get('id', 'unknown')}.pdf", pdf_file, 'application/pdf')
                }
                
                # Prepare metadata
                data = {
                    'collection': 'factures_pdf',
                    'filename_download': f"facture_{current_date}-{facture_data.get('id', 'unknown')}.pdf",
                    'title': f"Facture n°{current_date}-{facture_data.get('id', 'unknown')}",
                    'description': f"PDF généré pour la facture n°{current_date}-{facture_data.get('id', 'unknown')}",
                    'facture_id': str(facture_data.get('id', '')),
                    'client_nom': facture_data.get('client', {}).get('first_name', ''),
                    'date_generation': datetime.now().isoformat(),
                    'folder': 'c571fa44-dc5d-4173-9c3e-de62e12ace2e'
                }
                
                headers = {
                    'Authorization': f'Bearer {self.directus_token}'
                }
                
                # Send to Directus
                response = requests.post(
                    f"{self.directus_api_url}/files",
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=60
                )
                
                if response.status_code in [200, 201]:
                    # Extract the file id from the response
                    file_id = response.json().get('data', {}).get('id')
                    logger.info(f"Directus file id: {file_id}")
                    logger.info(f"PDF successfully sent to Directus")

                    # update the facture with the file id
                    response = requests.patch(
                        f"{self.directus_api_url}/items/Factures/{facture_data.get('id', '')}",
                        json={'file': file_id, 'montant_ttc': grand_total, 'montant': subtotal},
                        headers=headers,
                        timeout=60
                    )
                    if response.status_code == 200:
                        logger.info(f"Facture {facture_data.get('id', '')} updated with file id {file_id}")
                    else:
                        logger.error(f"Failed to update facture {facture_data.get('id', '')} with file id {file_id}")
                        return False

                    return True
                else:
                    logger.error(f"Failed to send PDF to Directus. Status: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    return False
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending PDF to Directus: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending PDF to Directus: {e}")
            return False
    
    def cleanup_temp_file(self, pdf_path: str):
        """
        Clean up temporary PDF file.
        
        Args:
            pdf_path: Path to the temporary PDF file
        """
        try:
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
                logger.info(f"Temporary file cleaned up: {pdf_path}")
        except Exception as e:
            logger.warning(f"Could not clean up temporary file {pdf_path}: {e}")
    
    def process_factures(self, id: Optional[str] = None) -> Dict[str, int]:
        """
        Main method to process all factures: retrieve, generate PDFs, and send to Directus.
        
        Returns:
            Dictionary with processing statistics
        """
        stats = {
            'total_factures': 0,
            'successful_pdfs': 0,
            'successful_uploads': 0,
            'errors': 0
        }
        
        try:
            # Retrieve factures
            factures = self.retrieve_factures(id)
            stats['total_factures'] = len(factures)
            
            if not factures:
                logger.warning("No factures found to process")
                return stats
            
            # Process each facture
            for facture in factures:
                try:
                    # Generate PDF
                    result = self.generate_pdf(facture)
                    if result:
                        pdf_path, grand_total, subtotal = result
                        stats['successful_pdfs'] += 1
                        
                        # Log the totals
                        logger.info(f"Facture {facture.get('id', 'unknown')} - Subtotal: {subtotal}$, Grand Total: {grand_total}$")
                        
                        # Send to Directus
                        if self.send_to_directus(pdf_path, facture, grand_total, subtotal):
                            stats['successful_uploads'] += 1
                            logger.info(f"Successfully processed facture {facture.get('id', 'unknown')}")
                        else:
                            stats['errors'] += 1
                            logger.error(f"Failed to upload PDF for facture {facture.get('id', 'unknown')}")
                        
                        # Clean up temporary file
                        self.cleanup_temp_file(pdf_path)
                    else:
                        stats['errors'] += 1
                        logger.error(f"Failed to generate PDF for facture {facture.get('id', 'unknown')}")
                        
                except Exception as e:
                    stats['errors'] += 1
                    logger.error(f"Error processing facture {facture.get('id', 'unknown')}: {e}")
            
            # Log final statistics
            logger.info("Processing completed. Statistics:")
            logger.info(f"Total factures: {stats['total_factures']}")
            logger.info(f"Successful PDFs: {stats['successful_pdfs']}")
            logger.info(f"Successful uploads: {stats['successful_uploads']}")
            logger.info(f"Errors: {stats['errors']}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Unexpected error during processing: {e}")
            stats['errors'] += 1
            return stats


def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.json file.
    
    Returns:
        Configuration dictionary
    """
    config_path = 'config.json'
    
    if not os.path.exists(config_path):
        # Create default config
        default_config = {
            "dropcolis_api_url": "https://services.dropcolis.ca",
            "directus_api_url": "https://your-directus-instance.com",
            "directus_token": "your-directus-token-here",
            "template_path": "facture_template.html"
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        logger.warning(f"Created default config file: {config_path}")
        logger.warning("Please update the configuration with your actual API endpoints and tokens")
        return default_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise


def main():
    """
    Main function to run the facture generation process.
    """
    try:
        logger.info("Starting Facture Generation Process")
        
        # Load configuration
        config = load_config()
        
        # Validate required configuration
        required_fields = ['dropcolis_api_url', 'directus_api_url', 'directus_token', 'template_path']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required configuration fields: {missing_fields}")
            logger.error("Please update your config.json file")
            return
        
        # Check if template exists
        if not os.path.exists(config['template_path']):
            logger.error(f"HTML template not found: {config['template_path']}")
            return
        
        # Initialize generator
        generator = FactureGenerator(config)
        
        # Process factures
        stats = generator.process_factures()
        
        # Exit with appropriate code
        if stats['errors'] == 0:
            logger.info("All factures processed successfully!")
            exit(0)
        else:
            logger.warning(f"Processing completed with {stats['errors']} errors")
            exit(1)
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        exit(1)


if __name__ == "__main__":
    main()
