# MTL Generation Prompt for ChatGPT
*Slot Machine Technical Procedures for EG TECHS*

## Understanding the MTL System

This MTL system is designed for **Electronic Gaming (EG) Technicians** who service slot machines across multiple casino properties. The work environment involves:

- **12-14 different slot machine vendors** (IGT, Konami, Light & Wonder, ATI, SegaSammy, Everi, etc.)
- **20-30+ models per vendor** with unique procedures
- **Complex technical procedures** requiring precision and documentation
- **Training progression system** using standardized documentation

### MTL Types & Purpose:
- **MTL 1**: Quick reference notes/cheat sheet for experienced techs
- **MTL 2**: Detailed walkthrough with pictures and comprehensive steps for training
- **MTL 3**: Teachback form (assessment version based on MTL 1 with verification elements)

## Prompt Template:

```
I need you to create an MTL (Master Task List) JSON for slot machine technicians. This will be used to train EG TECHS who service gaming equipment across multiple casino properties.

**Context:** We work with 12-14 different slot machine vendors (IGT, Konami, Light & Wonder, ATI, SegaSammy, Everi, etc.), each with 20-30+ models. Our technicians need standardized procedures for complex technical tasks.

**Procedure:** [DESCRIBE THE SPECIFIC SLOT MACHINE PROCEDURE - e.g., "JCM GEN5 printer firmware flashing", "MEI bill validator cleaning", "IGT S2000 RAM clear procedure", "Konami diagnostic menu navigation"]

**MTL Type:** [Specify MTL 1 (quick reference), MTL 2 (detailed training), or MTL 3 (teachback assessment)]

**Requirements:**
1. Use the provided JSON template structure
2. MTL_NUMBER must be "MTL 1", "MTL 2", or "MTL 3" only (training progression system)
3. Create 8-15 actionable steps for trained technicians
3. Include vendor-specific details and model numbers where applicable
4. Add safety considerations for electrical/mechanical work
5. Include prerequisite knowledge (certifications, prior procedures)
6. Specify completion criteria and verification steps
7. Add troubleshooting for common issues
8. Use proper MTL numbering (MTL 1/2/3 for type, GT-### for version)
9. Remove all _HELP fields from final JSON
10. Focus on casino gaming environment specifics

**Technical Focus Areas:**
- Bill validators, printers, and peripherals
- Diagnostic procedures and error codes  
- Player tracking systems and SAS protocols
- Cabinet maintenance and hardware replacement
- Firmware updates and RAM clear procedures
- Progressive systems (WAP/Linked/Standalone)
- Controller and signage systems
- Game conversions and installations

**JSON Template:**
[PASTE THE CLEAN TEMPLATE HERE]

Please create a comprehensive MTL JSON that follows our technical standards.
```

## Example Usage Scenarios:

### For Equipment Procedures:
"Create an MTL for installing and configuring a new wireless access point in a corporate environment"

### For Software Procedures:
"Create an MTL for deploying a software update to workstations using SCCM"

### For Maintenance Procedures:
"Create an MTL for quarterly maintenance on industrial printers"

### For Security Procedures:
"Create an MTL for onboarding a new employee in the security system"

## Quick Start Examples:

### Example 1: Network Equipment
```
Procedure: "Configure a Cisco 2960 switch for a new VLAN deployment"
Expected Output: 10-12 steps covering physical setup, console access, VLAN configuration, testing
```

### Example 2: Software Installation
```
Procedure: "JCM GEN5 thermal printer head cleaning and paper path maintenance"
Expected Output: 8-10 steps covering power down, access panels, cleaning process, testing
```

### Example 2: Diagnostic Testing
```
Procedure: "IGT S2000 RAM clear procedure after motherboard replacement"
Expected Output: 10-12 steps covering power sequence, diagnostic menu access, RAM clear, verification
```

### Example 3: Player Tracking
```
Procedure: "SAS cable installation and player tracking switch configuration for new game installation"
Expected Output: 6-8 steps covering cable routing, switch settings, communication testing
```

## Tips for Best Results:

1. **Be Vendor Specific**: Instead of "printer maintenance," say "JCM GEN5 thermal printer preventive maintenance"

2. **Include Model Numbers**: "IGT S2000", "Konami KX43", "Light & Wonder TwinStar J43" 

3. **Specify Environment**: "casino floor environment", "back-of-house maintenance", "high-volume gaming area"

4. **Include Regulatory Context**: "NOM/ERFC seal break procedures", "jurisdiction compliance requirements"

5. **Mention Technical Standards**: "following SAS protocol specifications" or "per manufacturer service bulletins"

## Post-Generation Checklist:

After ChatGPT generates the MTL JSON:
- [ ] All _HELP fields removed
- [ ] MTL_NUMBER is "MTL 1", "MTL 2", or "MTL 3" only (training progression system)
- [ ] VERSION_NUMBER follows GT-### format (e.g., GT-001, GT-045)
- [ ] Steps are actionable and specific
- [ ] Safety considerations included if needed
- [ ] STEPS array has 8-15 items
- [ ] JSON is valid (no syntax errors)
- [ ] Ready to import into MTL generator
