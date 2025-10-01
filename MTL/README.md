# MTL Document Generator - EG TECH Training System

A comprehensive Python-based tool for generating professional Master Task List (MTL) documents from JSON data using templates. This system is specifically designed for **Electronic Gaming (EG) Technicians** who service slot machines across multiple casino properties, supporting 12-14+ different vendors with 20-30+ models each.

## 🎯 **What This Does**

This system enables EG TECH trainers and supervisors to create standardized technical documentation for slot machine procedures. It takes JSON data for specific procedures and generates professional Word documents using your existing templates. 

### **MTL Training Progression System:**
- **MTL 1**: Quick reference notes/cheat sheets for experienced technicians
- **MTL 2**: Detailed walkthrough procedures with comprehensive steps for training
- **MTL 3**: Teachback assessment forms (based on MTL 1 with verification elements)

### **Automated Features:**
- Finds and replaces placeholders in templates (like `{MTL_#}`, `{MTL_TITLE}`, etc.)
- Populates tables with step-by-step technical procedures
- Preserves your template's formatting, images, and layout  
- Handles vendor-specific model information and safety requirements

## ✨ **Key Features**

- 🔄 **Smart Template Processing**: Automatically detects and works with your specific placeholder format
- 📊 **Advanced Table Handling**: Intelligently identifies and populates step tables
- 🖥️ **Multiple Interfaces**: GUI, command-line, and batch processing options
- � **Template Analysis**: Analyzes your templates to understand their structure
- 📄 **Format Preservation**: Maintains your template's formatting and layout
- ✅ **Robust Error Handling**: Comprehensive validation and error reporting
- 🚀 **Batch Processing**: Handle multiple documents at once

## 🚀 **Quick Start**

### Option 1: Ultimate GUI (Recommended)
```bash
python ultimate_mtl_gui.py
```
This gives you a complete graphical interface with template analysis, document generation, and JSON preview.

### Option 2: Custom Generator (Your Template Format)
```bash
python custom_mtl_generator.py
```
This is specifically designed for your template with `{MTL_#}` and `{MTL_TITLE}` placeholders.

### Option 3: Command Line
```bash
python template_processor.py --json mtl1_data.json --template MTL1_MasterTemplate_Placeholders.docx
```

## 📁 **File Structure**

```
MTL/
├── ultimate_mtl_gui.py         # 🎯 Main GUI interface (recommended)
├── custom_mtl_generator.py     # 🔧 Custom generator for your template
├── template_processor.py       # 📋 Template analyzer & CLI
├── enhanced_mtl_generator.py   # ⚙️ Enhanced processing engine
├── mtl_generator.py           # 🔄 Original generator
├── batch_mtl_generator.py     # 📦 Batch processing
├── mtl_gui.py                 # 🖥️ Simple GUI
├── mtl1_data.json             # 📄 Sample data
├── example_network_data.json  # 📄 Example data
├── config.json                # ⚙️ Configuration
├── requirements.txt           # 📦 Dependencies
└── README.md                  # 📖 This file
```

## 📊 **Your Template Analysis Results**

Based on your `MTL1_MasterTemplate_Placeholders.docx`:
- **Placeholders Found**: `{MTL_#}`, `{MTL_TITLE}`
- **Tables**: 2 tables (1 steps table, 1 data table)
- **Structure**: Professional layout with header and formatted tables

## 📝 **JSON Data Format**

Your JSON data should follow this structure:

```json
{
  "MTL_NUMBER": "MTL 2",
  "MTL_TITLE": "JCM GEN5 Printer Flashing",
  "VERSION_NUMBER": "GT-002", 
  "REVISION_NUMBER": "001",
  "CREATED_DATE": "06/2024",
  "CREATED_BY": "Yancy Shepherd",
  "STEPS": [
    "Step 1 description",
    "Step 2 description",
    "Step 3 description"
  ]
}
```

## 🎯 **Supported Placeholder Formats**

The system automatically recognizes these placeholder formats:
- `{MTL_#}` → Your MTL number
- `{MTL_TITLE}` → Document title
- `{{mtl_number}}` → Alternative format
- `{{title}}` → Alternative format
- `[mtl_number]` → Bracket format
- And more...

## 🚀 **Usage Examples**

### Generate Document with GUI
1. Run `python ultimate_mtl_gui.py`
2. Select your JSON file and template
3. Click "Generate Document"
4. Your formatted document is ready!

### Analyze Template Structure
```bash
python template_processor.py --analyze MTL1_MasterTemplate_Placeholders.docx
```

### Batch Process Multiple Files
```bash
python batch_mtl_generator.py --batch
```

### Generate with Custom Output Name
```bash
python custom_mtl_generator.py
```

## 🔧 **What's Generated**

✅ **Successfully Generated Documents**:
- `MTL_2_Final_YYYYMMDD_HHMMSS.docx` - Your printer flashing procedure
- `MTL_3_Final_YYYYMMDD_HHMMSS.docx` - Network switch configuration
- All with your template's formatting and layout preserved

## 🎨 **Customization**

### Adding New Data Fields
1. Add the field to your JSON data
2. Add a placeholder to your Word template
3. The system will automatically map them

### Custom Placeholder Formats
The system supports multiple formats automatically. Your template uses `{MTL_#}` and `{MTL_TITLE}` which are fully supported.

## 🔍 **Troubleshooting**

### Common Issues

1. **"Template not found" error**
   - Ensure the template file exists and is accessible
   - Check the file path is correct

2. **"Placeholders not replaced" error**
   - Use the template analyzer to see what placeholders are found
   - Ensure your JSON data has the matching fields

3. **"Steps not appearing" error**
   - Ensure your JSON has a "steps" array
   - The system automatically detects step tables

### Getting Help

1. Use the Ultimate GUI's "Analyze Template" feature
2. Check the output console for detailed processing information
3. Verify your JSON data format matches the expected structure

## 🎉 **Success Stories**

✅ **Your Template**: Successfully analyzed and processed with `{MTL_#}` and `{MTL_TITLE}` placeholders  
✅ **Steps Table**: Automatically identified and populated with 10 steps  
✅ **Formatting**: Template layout and formatting preserved  
✅ **Multiple Data Sets**: Works with different JSON data files  

## 🚀 **What's Next**

Your system is now ready for production use! You can:
1. Create new JSON files for different procedures
2. Use the same template for consistent formatting
3. Batch process multiple documents at once
4. Customize the templates further if needed

## 📞 **Support**

If you need help or want to add features:
1. Use the template analyzer to understand your documents
2. Check the console output for detailed processing information
3. The system is designed to be robust and handle various formats automatically
