import sys
import os
import json
import logging
from pathlib import Path
import shutil
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add parent directory to path to import final_mtl_generator
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

try:
    from final_mtl_generator import FinalMTLGenerator
    logger.info("Successfully imported FinalMTLGenerator")
except ImportError as e:
    logger.error(f"Error importing FinalMTLGenerator: {e}")
    raise

def get_mtl_templates():
    """Get template mapping for each MTL type with improved fallback logic."""
    template_folder = os.path.join(parent_dir, 'templates')
    logger.debug(f"Looking for templates in: {template_folder}")
    
    # Check if template folder exists
    if not os.path.exists(template_folder):
        logger.error(f"Template folder not found: {template_folder}")
        raise FileNotFoundError(f"Template folder not found: {template_folder}")
    
    # Primary template paths
    mtl_templates = {
        'MTL1': os.path.join(template_folder, 'MTL1 Template GT-00X-0X.docx'),
        'MTL2': os.path.join(template_folder, 'MTL2 Template GT-00X-0X.docx'), 
        'MTL3': os.path.join(template_folder, 'MTL3 Template GT-00X-0X.docx'),
    }
    
    # List all files in template folder for debugging
    all_files = os.listdir(template_folder)
    logger.debug(f"All files in template folder: {all_files}")
    
    # Find DOCX files that might be templates
    docx_files = [f for f in all_files if f.endswith('.docx')]
    logger.debug(f"DOCX files in template folder: {docx_files}")
    
    # Check if templates exist, if not look for alternative names
    valid_templates = {}
    for mtl_type, template_path in mtl_templates.items():
        if os.path.exists(template_path):
            logger.info(f"Found template for {mtl_type}: {template_path}")
            valid_templates[mtl_type] = template_path
        else:
            logger.warning(f"Primary template not found for {mtl_type}: {template_path}")
            
            # Try alternative naming patterns
            alt_patterns = [
                # Standard variations
                os.path.join(template_folder, f'{mtl_type} Template.docx'),
                os.path.join(template_folder, f'{mtl_type}_Template.docx'),
                os.path.join(template_folder, f'{mtl_type}.docx'),
                # Case-insensitive match
                *[os.path.join(template_folder, f) for f in docx_files 
                  if mtl_type.lower() in f.lower() and 'template' in f.lower()]
            ]
            
            found = False
            for alt_path in alt_patterns:
                if os.path.exists(alt_path):
                    valid_templates[mtl_type] = alt_path
                    logger.info(f"Using alternative template for {mtl_type}: {alt_path}")
                    found = True
                    break
            
            if not found:
                logger.warning(f"No template found for {mtl_type} after trying alternatives")
    
    # If no valid templates found, log a clear error
    if not valid_templates:
        logger.error("No valid templates found in template folder")
        raise FileNotFoundError("No valid templates found. Please check the templates folder.")
    
    logger.info(f"Found {len(valid_templates)} valid templates: {list(valid_templates.keys())}")
    return valid_templates

def convert_docx_to_pdf(docx_path, pdf_path):
    """Convert DOCX to PDF using LibreOffice."""
    try:
        logger.debug(f"Converting DOCX to PDF: {docx_path} -> {pdf_path}")
        subprocess.run([
            "soffice", "--headless", "--convert-to", "pdf", "--outdir",
            os.path.dirname(pdf_path), docx_path
        ], check=True, capture_output=True, text=True)
        
        # LibreOffice generates PDF with same name as DOCX but .pdf extension
        generated_pdf = os.path.join(
            os.path.dirname(pdf_path),
            os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
        )
        
        # Move to desired location if different
        if generated_pdf != pdf_path and os.path.exists(generated_pdf):
            shutil.move(generated_pdf, pdf_path)
            logger.debug(f"Moved generated PDF to: {pdf_path}")
        
        return os.path.exists(pdf_path)
    except subprocess.CalledProcessError as e:
        logger.error(f"LibreOffice PDF conversion failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during PDF conversion: {e}")
        return False

def generate_mtl_document(json_file, mtl_type, output_dir, revision='1', filetype='pdf'):
    """Generate a single MTL document (DOCX and/or PDF).
    
    Args:
        json_file: Path to JSON file
        mtl_type: MTL type to generate (MTL1, MTL2, MTL3)
        output_dir: Directory to save files
        revision: Revision number to be added to the document
        filetype: Output format ('pdf', 'docx', or 'both')
        
    Returns:
        Dictionary with generated file paths
    """
    logger.debug(f"Generating {mtl_type} from {json_file}, revision: {revision}, filetype: {filetype}")
    
    # Get template mapping
    mtl_templates = get_mtl_templates()
    template_path = mtl_templates.get(mtl_type)
    
    if not template_path:
        logger.error(f"No template found for {mtl_type}")
        logger.debug(f"Available templates: {list(mtl_templates.keys())}")
        logger.debug(f"Template folder: {os.path.join(parent_dir, 'templates')}")
        raise FileNotFoundError(f"Template not found for {mtl_type}. Available templates: {list(mtl_templates.keys())}")
    
    if not os.path.exists(template_path):
        logger.error(f"Template file doesn't exist: {template_path}")
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    try:
        # Initialize generator with JSON data
        logger.debug(f"Loading JSON data from {json_file}")
        generator = FinalMTLGenerator(json_file)
        
        # Patch revision and current date into the data
        generator.data['REVISION_NUMBER'] = revision
        generator.data['CREATED_DATE'] = datetime.now().strftime('%m-%d-%Y')
        
        # Create output paths
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        output_docx = os.path.join(output_dir, f"{base_name}_{mtl_type}_rev{revision}.docx")
        output_pdf = os.path.join(output_dir, f"{base_name}_{mtl_type}_rev{revision}.pdf")
        
        # Generate DOCX
        logger.debug(f"Creating DOCX: {output_docx} using template: {template_path}")
        generator.generate_document(template_path=template_path, output_path=output_docx)
        
        if not os.path.exists(output_docx):
            logger.error(f"DOCX file was not created at {output_docx}")
            raise FileNotFoundError(f"Failed to create DOCX file: {output_docx}")
        
        result = {'docx': output_docx}
        
        # Generate PDF if requested
        if filetype in ['pdf', 'both']:
            logger.debug(f"Converting DOCX to PDF: {output_docx} -> {output_pdf}")
            if convert_docx_to_pdf(output_docx, output_pdf):
                logger.info(f"Generated PDF: {output_pdf}")
                result['pdf'] = output_pdf
            else:
                logger.warning(f"Failed to generate PDF for {mtl_type}")
                if 'pdf' in result:
                    del result['pdf']
        
        # Clean up DOCX if only PDF was requested
        if filetype == 'pdf' and result.get('pdf') and os.path.exists(output_docx):
            logger.debug(f"Removing temporary DOCX file: {output_docx}")
            os.remove(output_docx)
            if 'docx' in result:
                del result['docx']
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating {mtl_type} from {json_file}: {e}", exc_info=True)
        raise

def generate_mtl_pdfs(json_files, mtl_types, output_dir, revision='1'):
    """Generate PDFs from JSON files (legacy function for compatibility).
    
    Args:
        json_files: List of JSON file paths
        mtl_types: List of MTL types to generate (MTL1, MTL2, MTL3)
        output_dir: Directory to save PDFs
        revision: Revision number to be added to the document
        
    Returns:
        List of generated PDF file paths
    """
    logger.debug(f"Generating PDFs for {len(json_files)} files, types: {mtl_types}, revision: {revision}")
    output_files = []
    
    for json_file in json_files:
        try:
            logger.debug(f"Processing file: {json_file}")
            for mtl_type in mtl_types:
                logger.debug(f"Generating {mtl_type} for {os.path.basename(json_file)}")
                
                result = generate_mtl_document(json_file, mtl_type, output_dir, revision, 'pdf')
                
                if result.get('pdf'):
                    output_files.append(result['pdf'])
                if result.get('docx'):
                    output_files.append(result['docx'])
                    
        except Exception as e:
            logger.error(f"Error processing {json_file}: {e}")
            continue
    
    logger.info(f"Generated {len(output_files)} files")
    return output_files