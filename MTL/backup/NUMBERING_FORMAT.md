# 📋 MTL Numbering Format - CORRECTED

## ✅ **Correct Numbering Format**

### MTL_NUMBER Format: "MTL #" only 3 MTL's
- **MTL 1** - First MTL document
- **MTL 2** - Second MTL document  
- **MTL 3** - Third MTL document

### VERSION_NUMBER Format: "GT-###" GT-### will change with each new task
- **GT-001** - First procedure version
- **GT-002** - Second procedure version
- **GT-045** - Forty-fifth procedure version
- **GT-150** - One hundred fiftieth procedure version

## 📊 **Example JSON Structure**

```json
{
  "MTL_NUMBER": "MTL 1",           // Document sequence number
  "MTL_TITLE": "JCM GEN5 Printer Flashing",
  "VERSION_NUMBER": "GT-002",      // Procedure version number
  "REVISION_NUMBER": "001",        // Revision of this version
  "CREATED_DATE": "06/2024",
  "CREATED_BY": "Yancy Shepherd",
  "STEPS": [...]
}
```

## 🔍 **Key Differences**

| Field | Format | Purpose | Example |
|-------|--------|---------|---------|
| `MTL_NUMBER` | "MTL #" | Document ID in sequence | MTL 1, MTL 2, MTL 3 |
| `VERSION_NUMBER` | "GT-###" | Procedure version | GT-001, GT-045 |
| `REVISION_NUMBER` | "###" | Revision of version | 001, 002, 003 |

## 💡 **Usage Logic**

- **MTL_NUMBER**: Sequential document numbering across all MTLs
- **VERSION_NUMBER**: Tracks different versions of procedures
- **REVISION_NUMBER**: Updates to the same procedure version

## 🎯 **Updated Templates**

All templates have been corrected:
- ✅ `mtl_template.json` - Full template with help
- ✅ `mtl_clean_template.json` - Clean template for ChatGPT
- ✅ `mtl1_data.json` - Your printer procedure
- ✅ `example_router_mtl.json` - Router configuration example
- ✅ ChatGPT prompt guides updated
- ✅ Workflow documentation updated

## 🚀 **Generated Documents**

The system now correctly generates:
- **File names**: "MTL 2_Final_YYYYMMDD_HHMMSS.docx"
- **Document headers**: Shows "MTL 2" in template
- **Footer metadata**: All correct numbering
- **Template placeholders**: Properly replaced

Your numbering system is now consistent and professional! 🎉
