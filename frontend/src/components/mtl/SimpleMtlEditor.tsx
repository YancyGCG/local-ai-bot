import { useCallback, useEffect, useState } from 'react';
import '../../styles/global.css';

// Beautiful MTL Editor v3.0 - Cache Bust
interface SimpleMtlEditorProps {
  value?: Record<string, unknown>;
  onChange: (value: Record<string, unknown>) => void;
  onValidationChange?: (isValid: boolean, messages: string[]) => void;
}

const REQUIRED_FIELDS = ['MTL_TITLE', 'MTL_NUMBER', 'VERSION_NUMBER', 'REVISION_NUMBER', 'CREATED_BY', 'STEPS'];
const DEFAULT_CATEGORIES = ['Maintenance and Repair', 'Safety Procedures', 'Installation', 'Training', 'Quality Control', 'Operations'];

const SimpleMtlEditor = ({ value, onChange, onValidationChange }: SimpleMtlEditorProps) => {
  const [localValue, setLocalValue] = useState<Record<string, unknown>>(value || {});
  const [categories, setCategories] = useState<string[]>(DEFAULT_CATEGORIES);

  useEffect(() => {
    if (value) {
      setLocalValue(value);
    }
  }, [value]);

  const handleChange = useCallback((field: string, newValue: unknown) => {
    const updated = { ...localValue, [field]: newValue };
    setLocalValue(updated);
    onChange(updated);
    
    // Simple validation
    const missing = REQUIRED_FIELDS.filter(f => !updated[f] || (Array.isArray(updated[f]) && (updated[f] as unknown[]).length === 0));
    const valid = missing.length === 0;
    onValidationChange?.(valid, missing.map(f => `${f} is required`));
  }, [localValue, onChange, onValidationChange]);

  const handleArrayChange = useCallback((field: string, index: number, newValue: string) => {
    const currentArray = Array.isArray(localValue[field]) ? [...(localValue[field] as unknown[])] : [];
    currentArray[index] = newValue;
    handleChange(field, currentArray);
  }, [localValue, handleChange]);

  const addArrayItem = useCallback((field: string) => {
    const currentArray = Array.isArray(localValue[field]) ? [...(localValue[field] as unknown[])] : [];
    currentArray.push('');
    handleChange(field, currentArray);
  }, [localValue, handleChange]);

  const removeArrayItem = useCallback((field: string, index: number) => {
    const currentArray = Array.isArray(localValue[field]) ? [...(localValue[field] as unknown[])] : [];
    currentArray.splice(index, 1);
    handleChange(field, currentArray);
  }, [localValue, handleChange]);

  const handleObjectChange = useCallback((field: string, key: string, newValue: string) => {
    const currentObj = (localValue[field] && typeof localValue[field] === 'object' && !Array.isArray(localValue[field])) 
      ? { ...(localValue[field] as Record<string, unknown>) } 
      : {};
    if (newValue) {
      currentObj[key] = newValue;
    } else {
      delete currentObj[key];
    }
    handleChange(field, currentObj);
  }, [localValue, handleChange]);

  const addObjectItem = useCallback((field: string) => {
    const currentObj = (localValue[field] && typeof localValue[field] === 'object' && !Array.isArray(localValue[field])) 
      ? { ...(localValue[field] as Record<string, unknown>) } 
      : {};
    currentObj[`new_key_${Date.now()}`] = '';
    handleChange(field, currentObj);
  }, [localValue, handleChange]);

  const renderCategoryField = (field: string, label: string, tabIdx?: number) => {
    const [isCustom, setIsCustom] = useState(false);
    const currentValue = String(localValue[field] || '');
    const isInList = categories.includes(currentValue);
    
    return (
      <div key={field} style={{ marginBottom: '20px' }}>
        <label style={{ 
          display: 'block', 
          marginBottom: '8px', 
          fontWeight: '600', 
          color: '#374151',
          fontSize: '14px'
        }}>
          {label} {REQUIRED_FIELDS.includes(field) && <span style={{ color: '#dc2626' }}>*</span>}
        </label>
        {!isCustom && isInList ? (
          <div style={{ display: 'flex', gap: '12px' }}>
            <select
              value={currentValue}
              onChange={(e) => {
                if (e.target.value === 'custom') {
                  setIsCustom(true);
                } else {
                  handleChange(field, e.target.value);
                }
              }}
              tabIndex={tabIdx}
              style={{
                flex: 1,
                padding: '10px 14px',
                background: '#ffffff',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                color: '#111827',
                fontSize: '14px',
                transition: 'border-color 0.15s ease-in-out'
              }}
              onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
              onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
            >
              <option value="">Select category...</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
              <option value="custom">+ Add New Category</option>
            </select>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              value={currentValue}
              onChange={(e) => handleChange(field, e.target.value)}
              onBlur={(e) => {
                const newValue = e.target.value.trim();
                if (newValue && !categories.includes(newValue)) {
                  setCategories(prev => [...prev, newValue]);
                }
                setIsCustom(false);
              }}
              tabIndex={tabIdx}
              placeholder="Enter new category"
              style={{
                flex: 1,
                padding: '10px 14px',
                background: '#ffffff',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                color: '#111827',
                fontSize: '14px',
                transition: 'border-color 0.15s ease-in-out'
              }}
              onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
            />
            <button
              type="button"
              onClick={() => setIsCustom(false)}
              style={{
                padding: '10px 14px',
                background: '#f3f4f6',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                color: '#374151',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.15s ease-in-out'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#e5e7eb'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#f3f4f6'}
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    );
  };

  const renderStringField = (field: string, label: string, tabIdx?: number) => (
    <div key={field} style={{ marginBottom: '20px' }}>
      <label style={{ 
        display: 'block', 
        marginBottom: '8px', 
        fontWeight: '600', 
        color: '#374151',
        fontSize: '14px'
      }}>
        {label} {REQUIRED_FIELDS.includes(field) && <span style={{ color: '#dc2626' }}>*</span>}
      </label>
      <input
        type="text"
        value={String(localValue[field] || '')}
        onChange={(e) => handleChange(field, e.target.value)}
        tabIndex={tabIdx}
        style={{
          width: '100%',
          padding: '10px 14px',
          background: '#ffffff',
          border: '1px solid #d1d5db',
          borderRadius: '8px',
          color: '#111827',
          fontSize: '14px',
          transition: 'border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out'
        }}
        onFocus={(e) => {
          e.target.style.borderColor = '#3b82f6';
          e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
        }}
        onBlur={(e) => {
          e.target.style.borderColor = '#d1d5db';
          e.target.style.boxShadow = 'none';
        }}
      />
    </div>
  );

  // Short field renderer for compact layouts
  const renderShortField = (field: string, label: string, tabIdx?: number, inputType: string = 'text') => (
    <div key={field} style={{ marginBottom: 0 }}>
      <label style={{ 
        display: 'block', 
        marginBottom: '8px', 
        fontWeight: '600', 
        color: '#374151', 
        fontSize: '14px' 
      }}>
        {label} {REQUIRED_FIELDS.includes(field) && <span style={{ color: '#dc2626' }}>*</span>}
      </label>
      <input
        type={inputType}
        value={String(localValue[field] || '')}
        onChange={(e) => handleChange(field, e.target.value)}
        tabIndex={tabIdx}
        placeholder={inputType === 'date' ? '' : inputType === 'text' && field === 'CREATED_DATE' ? 'MM/DD/YY' : ''}
        style={{
          width: '100%',
          padding: '8px 10px',
          background: '#ffffff',
          border: '1px solid #d1d5db',
          borderRadius: '6px',
          color: '#111827',
          fontSize: '14px',
          transition: 'border-color 0.15s ease-in-out'
        }}
        onFocus={(e) => {
          e.target.style.borderColor = '#3b82f6';
        }}
        onBlur={(e) => {
          e.target.style.borderColor = '#d1d5db';
        }}
      />
    </div>
  );

  const renderArrayField = (field: string, label: string) => {
    const array = Array.isArray(localValue[field]) ? (localValue[field] as unknown[]) : [];
    
    return (
      <div key={field} data-field={field} style={{ 
        marginBottom: '24px', 
        background: '#ffffff', 
        padding: '20px', 
        borderRadius: '12px',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <label style={{ 
            fontWeight: '600', 
            color: '#374151',
            fontSize: '16px'
          }}>
            {label} {REQUIRED_FIELDS.includes(field) && <span style={{ color: '#dc2626' }}>*</span>}
          </label>
          <button
            type="button"
            onClick={() => addArrayItem(field)}
            style={{
              padding: '8px 16px',
              background: '#10b981',
              border: 'none',
              borderRadius: '6px',
              color: '#ffffff',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'background-color 0.15s ease-in-out'
            }}
            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#059669'}
            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#10b981'}
          >
            + Add Item
          </button>
        </div>
        <div style={{ border: '1px solid #e5e7eb', borderRadius: '8px', background: '#f9fafb' }}>
          {array.length === 0 ? (
            <div style={{ padding: '24px', color: '#6b7280', textAlign: 'center', fontSize: '14px' }}>
              No items yet. Click "Add Item" to get started.
            </div>
          ) : (
            array.map((item, index) => (
              <div key={index} style={{ 
                display: 'flex', 
                alignItems: 'flex-start', 
                padding: '12px', 
                borderBottom: index < array.length - 1 ? '1px solid #e5e7eb' : 'none',
                background: index % 2 === 0 ? '#ffffff' : '#f9fafb'
              }}>
                <span style={{ 
                  minWidth: '32px', 
                  color: '#6b7280', 
                  fontSize: '14px', 
                  fontWeight: '500',
                  paddingTop: '12px',
                  textAlign: 'center'
                }}>
                  {index + 1}.
                </span>
                <textarea
                  value={String(item || '')}
                  onChange={(e) => handleArrayChange(field, index, e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      addArrayItem(field);
                      setTimeout(() => {
                        const container = document.querySelector(`[data-field="${field}"]`);
                        if (container) {
                          const textareas = Array.from(container.querySelectorAll('textarea'));
                          const newTextarea = textareas[index + 1] as HTMLTextAreaElement;
                          if (newTextarea) {
                            newTextarea.focus();
                            newTextarea.setSelectionRange(0, 0);
                          }
                        }
                      }, 200);
                    }
                  }}
                  style={{
                    flex: 1,
                    margin: '0 12px',
                    padding: '8px 10px',
                    background: '#ffffff',
                    border: '1px solid #d1d5db',
                    borderRadius: '6px',
                    color: '#111827',
                    fontSize: '14px',
                    minHeight: '32px',
                    resize: 'vertical',
                    transition: 'border-color 0.15s ease-in-out'
                  }}
                  placeholder="Enter item content..."
                  onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
                  onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
                />
                <button
                  type="button"
                  onClick={() => removeArrayItem(field, index)}
                  style={{
                    padding: '8px 10px',
                    background: '#fee2e2',
                    border: '1px solid #fecaca',
                    borderRadius: '6px',
                    color: '#dc2626',
                    fontSize: '14px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease-in-out'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#fecaca';
                    e.currentTarget.style.borderColor = '#f87171';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = '#fee2e2';
                    e.currentTarget.style.borderColor = '#fecaca';
                  }}
                >
                  Remove
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  const renderObjectField = (field: string) => {
    const obj = (localValue[field] && typeof localValue[field] === 'object' && !Array.isArray(localValue[field])) 
      ? (localValue[field] as Record<string, unknown>) 
      : {};
    const entries = Object.entries(obj);
    
    return (
      <div key={field} style={{ marginBottom: '0' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <span style={{ 
            fontWeight: '500', 
            color: '#6b7280',
            fontSize: '14px'
          }}>Add problem-solution pairs for troubleshooting reference</span>
          <button
            type="button"
            onClick={() => addObjectItem(field)}
            style={{
              padding: '8px 16px',
              background: '#10b981',
              border: 'none',
              borderRadius: '6px',
              color: '#ffffff',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'background-color 0.15s ease-in-out'
            }}
            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#059669'}
            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#10b981'}
          >
            + Add Problem
          </button>
        </div>
        <div style={{ border: '1px solid #e5e7eb', borderRadius: '8px', background: '#f9fafb' }}>
          {entries.length === 0 ? (
            <div style={{ padding: '24px', color: '#6b7280', textAlign: 'center', fontSize: '14px' }}>
              No troubleshooting items yet. Click "Add Problem" to get started.
            </div>
          ) : (
            entries.map(([key, val], index) => (
              <div key={key} style={{ 
                display: 'flex', 
                alignItems: 'flex-start', 
                gap: '12px',
                padding: '16px', 
                borderBottom: index < entries.length - 1 ? '1px solid #e5e7eb' : 'none',
                background: index % 2 === 0 ? '#ffffff' : '#f9fafb'
              }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', marginBottom: '6px', fontSize: '12px', fontWeight: '500', color: '#6b7280' }}>
                    Problem/Issue
                  </label>
                  <input
                    type="text"
                    value={key}
                    onChange={(e) => {
                      const newObj = { ...obj };
                      delete newObj[key];
                      if (e.target.value) {
                        newObj[e.target.value] = val;
                      }
                      handleChange(field, newObj);
                    }}
                    style={{
                      width: '100%',
                      padding: '6px 10px',
                      background: '#ffffff',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      color: '#111827',
                      fontSize: '14px'
                    }}
                    placeholder="Describe the problem or issue"
                  />
                </div>
                <div style={{ flex: 2 }}>
                  <label style={{ display: 'block', marginBottom: '6px', fontSize: '12px', fontWeight: '500', color: '#6b7280' }}>
                    Solution/Resolution
                  </label>
                  <textarea
                    value={String(val || '')}
                    onChange={(e) => handleObjectChange(field, key, e.target.value)}
                    style={{
                      width: '100%',
                      padding: '6px 10px',
                      background: '#ffffff',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      color: '#111827',
                      fontSize: '14px',
                      minHeight: '48px',
                      resize: 'vertical'
                    }}
                    placeholder="Provide the solution or resolution steps"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => {
                    const newObj = { ...obj };
                    delete newObj[key];
                    handleChange(field, newObj);
                  }}
                  style={{
                    padding: '8px 10px',
                    background: '#fee2e2',
                    border: '1px solid #fecaca',
                    borderRadius: '6px',
                    color: '#dc2626',
                    fontSize: '12px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    marginTop: '20px',
                    transition: 'all 0.15s ease-in-out'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#fecaca';
                    e.currentTarget.style.borderColor = '#f87171';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = '#fee2e2';
                    e.currentTarget.style.borderColor = '#fecaca';
                  }}
                >
                  Remove
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  return (
    <div style={{ background: '#f8fafc', minHeight: '100vh' }}>
      {/* Content Area */}
      <div className="content-container">
        <div className="content-card">
          <div style={{ marginBottom: '2px' }}>
        <h3 style={{ margin: '0 0 2px 0', color: '#1f2937', fontSize: '1.25rem', fontWeight: '600', borderBottom: '2px solid #f3f4f6', paddingBottom: '1px' }}>
          Document Information
        </h3>
        {renderStringField('MTL_TITLE', 'MTL Title', 1)}
      </div>

      {/* Three-column layout for numeric fields */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 1fr 1fr', 
        gap: '16px', 
        marginBottom: '24px', 
        background: '#f8fafc', 
        padding: '20px', 
        borderRadius: '12px',
        border: '2px solid #e2e8f0'
      }}>
        {renderShortField('MTL_NUMBER', 'MTL Number', 2)}
        {renderShortField('VERSION_NUMBER', 'Version', 3)}
        {renderShortField('REVISION_NUMBER', 'Revision', 4)}
      </div>

      {/* Two-column layout for creator information */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '2fr 1fr', 
        gap: '16px', 
        marginBottom: '24px', 
        background: '#f8fafc', 
        padding: '20px', 
        borderRadius: '12px',
        border: '2px solid #e2e8f0'
      }}>
        {renderShortField('CREATED_BY', 'Created By', 5)}
        {renderShortField('CREATED_DATE', 'Created Date', 6, 'text')}
      </div>
      
      <div style={{ 
        background: '#f8fafc', 
        padding: '20px', 
        borderRadius: '12px', 
        marginBottom: '28px',
        border: '2px solid #e2e8f0'
      }}>
        <h4 style={{ margin: '0 0 16px 0', color: '#374151', fontSize: '1.1rem', fontWeight: '600' }}>
          Project Details
        </h4>
        {renderCategoryField('CATEGORY', 'Category', 7)}
        {renderStringField('ESTIMATED_TIME', 'Estimated Time', 8)}
      </div>

      {/* Prerequisites and Preparation */}
      <div style={{ marginBottom: '32px' }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#1f2937', fontSize: '1.25rem', fontWeight: '600', borderBottom: '2px solid #f3f4f6', paddingBottom: '8px' }}>
          Prerequisites & Preparation
        </h3>
        {renderArrayField('PRE_REQS', 'Pre-Requisites')}
        {renderArrayField('EQUIPMENT_LIST', 'Equipment List')}
        {renderArrayField('REQUIRED_TOOLS', 'Required Tools')}
        {renderArrayField('EQUIPMENT_MODELS', 'Equipment Models')}
      </div>

      {/* Procedure Steps */}
      <div style={{ marginBottom: '32px' }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#1f2937', fontSize: '1.25rem', fontWeight: '600', borderBottom: '2px solid #f3f4f6', paddingBottom: '8px' }}>
          Procedure
        </h3>
        {renderArrayField('STEPS', 'Steps')}
        {renderArrayField('SAFETY_NOTES', 'Safety Notes')}
        {renderArrayField('COMPLETION_CRITERIA', 'Completion Criteria')}
      </div>

      {/* Additional Information */}
      <div style={{ marginBottom: '32px' }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#1f2937', fontSize: '1.25rem', fontWeight: '600', borderBottom: '2px solid #f3f4f6', paddingBottom: '8px' }}>
          Additional Information
        </h3>
        {renderArrayField('RELATED_PROCEDURES', 'Related Procedures')}
      </div>
      
      <div style={{ 
        background: '#f8fafc', 
        padding: '20px', 
        borderRadius: '12px',
        border: '1px solid #e2e8f0'
      }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#1f2937', fontSize: '1.25rem', fontWeight: '600', borderBottom: '2px solid #f3f4f6', paddingBottom: '8px' }}>
          Troubleshooting
        </h3>
        {renderObjectField('TROUBLESHOOTING')}
      </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleMtlEditor;
