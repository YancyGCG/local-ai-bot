#!/bin/bash

# Test script for Local AI Bot document processing

echo "🧪 Testing Local AI Bot Document Processing"
echo "==========================================="

# Check if the sample document exists
SAMPLE_DOC="examples/sample_document.md"

if [ ! -f "$SAMPLE_DOC" ]; then
    echo "❌ Sample document not found: $SAMPLE_DOC"
    exit 1
fi

echo "📄 Testing with sample document: $SAMPLE_DOC"
echo ""

# Test summary analysis
echo "🔍 Testing Summary Analysis..."
python3 src/document_processor.py --file "$SAMPLE_DOC" --analysis summary

echo ""
echo "🔍 Testing Breakdown Analysis..."
python3 src/document_processor.py --file "$SAMPLE_DOC" --analysis breakdown

echo ""
echo "🔍 Testing Questions Generation..."
python3 src/document_processor.py --file "$SAMPLE_DOC" --analysis questions

echo ""
echo "✅ All tests completed!"
echo ""
echo "💡 Try processing your own documents:"
echo "python3 src/document_processor.py --file /path/to/your/document.pdf"
