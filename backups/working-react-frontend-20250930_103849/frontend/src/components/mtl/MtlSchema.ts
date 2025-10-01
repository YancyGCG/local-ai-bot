import { JSONSchema7 } from 'json-schema';

export const mtlSchema: JSONSchema7 = {
  type: 'object',
  required: ['MTL_TITLE', 'MTL_NUMBER', 'VERSION_NUMBER', 'REVISION_NUMBER', 'CREATED_BY', 'STEPS'],
  properties: {
    MTL_TITLE: { type: ['string', 'number'], title: 'MTL Title' },
    MTL_NUMBER: { type: ['string', 'number'], title: 'MTL Number' },
    VERSION_NUMBER: { type: ['string', 'number'], title: 'Version' },
    REVISION_NUMBER: { type: ['string', 'number'], title: 'Revision' },
    CREATED_DATE: { type: ['string', 'number'], title: 'Created Date' },
    CREATED_BY: { type: ['string', 'number'], title: 'Created By' },
    CATEGORY: { type: ['string', 'number'], title: 'Category' },
    ESTIMATED_TIME: { type: ['string', 'number'], title: 'Estimated Time' },
    PRE_REQS: {
      type: 'array',
      title: 'Pre-Requisites',
      items: { type: ['string', 'number'] },
      default: []
    },
    EQUIPMENT_LIST: {
      type: 'array',
      title: 'Required Equipment',
      items: { type: ['string', 'number'] },
      default: []
    },
    COMPLETION_CRITERIA: {
      type: 'array',
      title: 'Completion Criteria',
      items: { type: ['string', 'number'] },
      default: []
    },
    STEPS: {
      type: 'array',
      title: 'Steps',
      items: { type: ['string', 'number'] },
      minItems: 1
    },
    SAFETY_NOTES: {
      type: 'array',
      title: 'Safety Notes',
      items: { type: ['string', 'number'] },
      default: []
    },
    REQUIRED_TOOLS: {
      type: 'array',
      title: 'Required Tools',
      items: { type: ['string', 'number'] },
      default: []
    },
    TROUBLESHOOTING: {
      type: 'object',
      title: 'Troubleshooting',
      additionalProperties: { type: ['string', 'number'] },
      default: {}
    },
    RELATED_PROCEDURES: {
      type: 'array',
      title: 'Related Procedures',
      items: { type: ['string', 'number'] },
      default: []
    },
    EQUIPMENT_MODELS: {
      type: 'array',
      title: 'Equipment Models',
      items: { type: ['string', 'number'] },
      default: []
    }
  },
  additionalProperties: true
};
