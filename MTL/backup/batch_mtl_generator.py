#!/usr/bin/env python3
"""
MTL Batch Generator - Command Line Interface

Usage:
    python batch_mtl_generator.py [options]
    
Options:
    --json-file PATH     Path to JSON data file (default: mtl1_data.json)
    --template PATH      Path to Word template file
    --output PATH        Output file path
    --batch              Process multiple JSON files
    --help               Show this help message
"""

import argparse
import os
import sys
import glob
from mtl_generator import MTLGenerator


def process_single_file(json_file, template_file=None, output_file=None):
    """Process a single JSON file."""
    try:
        generator = MTLGenerator(json_file)
        result = generator.generate_document(template_path=template_file, output_path=output_file)
        return True, result
    except Exception as e:
        return False, str(e)


def process_batch_files(json_pattern="*.json", template_file=None):
    """Process multiple JSON files matching a pattern."""
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print(f"No JSON files found matching pattern: {json_pattern}")
        return
    
    results = []
    for json_file in json_files:
        print(f"\nProcessing: {json_file}")
        success, result = process_single_file(json_file, template_file)
        
        if success:
            print(f"✅ Generated: {result}")
            results.append((json_file, result, "Success"))
        else:
            print(f"❌ Failed: {result}")
            results.append((json_file, None, result))
    
    # Summary
    print("\n" + "="*50)
    print("BATCH PROCESSING SUMMARY")
    print("="*50)
    for json_file, output_file, status in results:
        if status == "Success":
            print(f"✅ {json_file} → {output_file}")
        else:
            print(f"❌ {json_file} → Error: {status}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Word documents from JSON data using templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic usage with default files
    python batch_mtl_generator.py
    
    # Specify custom JSON file
    python batch_mtl_generator.py --json-file my_data.json
    
    # Use specific template and output file
    python batch_mtl_generator.py --json-file data.json --template template.docx --output result.docx
    
    # Process all JSON files in directory
    python batch_mtl_generator.py --batch
        """
    )
    
    parser.add_argument(
        '--json-file', 
        default='mtl1_data.json',
        help='Path to JSON data file (default: mtl1_data.json)'
    )
    
    parser.add_argument(
        '--template',
        help='Path to Word template file'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process all JSON files in current directory'
    )
    
    args = parser.parse_args()
    
    if args.batch:
        process_batch_files(template_file=args.template)
    else:
        if not os.path.exists(args.json_file):
            print(f"❌ JSON file not found: {args.json_file}")
            sys.exit(1)
        
        success, result = process_single_file(args.json_file, args.template, args.output)
        
        if success:
            print(f"✅ Document generated: {result}")
        else:
            print(f"❌ Error: {result}")
            sys.exit(1)


if __name__ == "__main__":
    main()
