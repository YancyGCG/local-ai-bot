# EG TECH MTL System - Updated for Slot Machine Technical Procedures

## 🎰 **System Overview**

This MTL (Master Task List) system is now specifically designed for **Electronic Gaming (EG) Technicians** who service slot machines across multiple casino properties. The system supports complex technical documentation for 12-14+ different vendors with 20-30+ models each.

## 📋 **MTL Training Progression System**

### **MTL 1 - Quick Reference**
- Concise cheat sheets for experienced technicians
- Essential steps without excessive detail
- Perfect for field reference during actual work

### **MTL 2 - Detailed Training**
- Comprehensive walkthrough procedures
- Includes pictures, detailed explanations, and context
- Used for initial training and skill development

### **MTL 3 - Teachback Assessment**
- Based on MTL 1 format with verification elements
- Includes assessment checkpoints and skill validation
- Used to confirm technician competency

## 🔧 **Technical Focus Areas**

The system now includes specialized support for:

### **Hardware & Peripherals**
- Bill validators (MEI, JCM, etc.)
- Thermal printers (JCM GEN5, etc.)
- Button panels and CSV testing
- Cabinet maintenance and hardware replacement

### **Diagnostic Procedures**
- Vendor-specific diagnostic menu navigation
- Error code resolution and troubleshooting
- RAM clear procedures after component replacement
- Reel strip testing and calibration

### **Player Tracking & Communications**
- SAS cable installation and configuration
- Player tracking switch setup (DHCP enabled, Smart vs Dummy)
- Communication protocol troubleshooting
- Ethernet vs Fiber connectivity

### **Progressive Systems**
- WAP (Wide Area Progressive)
- Linked progressive systems
- Standalone progressive configuration
- Progressive controller diagnostics

### **Regulatory Compliance**
- NOM/ERFC seal break procedures
- Jurisdiction-specific compliance requirements
- Gaming commission notification processes
- Documentation and verification requirements

## 📁 **Updated File Structure**

### **Templates & Examples**
- `mtl_template.json` - Full template with EG TECH context
- `mtl_clean_template.json` - Clean template for ChatGPT
- `example_jcm_printer_mtl.json` - Real-world slot machine procedure example

### **Documentation**
- `chatgpt_prompt_guide.md` - Updated prompts for slot machine procedures
- `README.md` - Updated with EG TECH context and training progression
- `WORKFLOW_GUIDE.md` - Includes slot machine specific workflow

### **Generators**
- `final_mtl_generator.py` - Enhanced with command-line argument support
- All other generators remain backward compatible

## 🎯 **ChatGPT Integration**

The ChatGPT prompt system now includes:

### **Vendor-Specific Context**
- IGT, Konami, Light & Wonder, ATI, SegaSammy, Everi procedures
- Model-specific details and part numbers
- Manufacturer service bulletin references

### **Casino Environment Awareness**
- Gaming floor considerations
- Back-of-house maintenance procedures  
- High-volume gaming area requirements
- Player disruption minimization

### **Safety & Compliance Focus**
- Electrical safety for 120V/240V systems
- Anti-static precautions for electronic components
- Gaming regulation compliance requirements
- Proper lockout/tagout procedures

## 🚀 **Ready-to-Use Examples**

### **Sample Procedures You Can Generate:**
- "JCM GEN5 printer firmware flashing and calibration"
- "MEI bill validator cleaning and error resolution"
- "IGT S2000 RAM clear after component replacement"
- "Konami diagnostic menu navigation and testing"
- "SAS cable installation and player tracking setup"
- "Progressive system diagnostics (WAP/Linked/Standalone)"
- "Cabinet hardware replacement with seal break procedures"

## ✅ **System Status**

- ✅ **Command-line arguments fixed** - Generator now accepts JSON file as parameter
- ✅ **EG TECH context added** - All documentation updated for slot machine environment
- ✅ **Real-world examples created** - JCM printer maintenance MTL as working example
- ✅ **ChatGPT prompts enhanced** - Vendor-specific and casino-focused prompts
- ✅ **Training progression documented** - MTL 1/2/3 system clearly defined
- ✅ **Backward compatibility maintained** - All existing features still work

The system is now ready for comprehensive slot machine technical documentation and EG TECH training workflows!
