const ARRAY_FIELDS = [
  'STEPS',
  'SAFETY_NOTES',
  'REQUIRED_TOOLS',
  'COMPLETION_CRITERIA',
  'PRE_REQS',
  'EQUIPMENT_LIST',
  'RELATED_PROCEDURES',
  'EQUIPMENT_MODELS'
];

const OBJECT_FIELDS = ['TROUBLESHOOTING'];

const DEFAULT_TEMPLATE: Record<string, unknown> = {
  MTL_TITLE: '',
  MTL_NUMBER: '',
  VERSION_NUMBER: '',
  REVISION_NUMBER: '',
  CREATED_DATE: '',
  CREATED_BY: '',
  CATEGORY: '',
  ESTIMATED_TIME: '',
  PRE_REQS: [],
  EQUIPMENT_LIST: [],
  COMPLETION_CRITERIA: [],
  STEPS: [],
  SAFETY_NOTES: [],
  REQUIRED_TOOLS: [],
  TROUBLESHOOTING: {},
  RELATED_PROCEDURES: [],
  EQUIPMENT_MODELS: []
};

const normalizeArrayField = (value: unknown): unknown[] => {
  if (Array.isArray(value)) {
    return (value as unknown[]).map((item) => (item === undefined ? '' : item));
  }
  if (value === undefined || value === null || value === '') {
    return [];
  }
  return [value];
};

export const sanitizeMtlTemplate = (raw: unknown): Record<string, unknown> => {
  const source = (!raw || typeof raw !== 'object') ? {} : (raw as Record<string, unknown>);
  const clone = JSON.parse(JSON.stringify({ ...DEFAULT_TEMPLATE, ...source })) as Record<string, unknown>;

  for (const field of ARRAY_FIELDS) {
    clone[field] = normalizeArrayField(clone[field]);
  }

  for (const field of OBJECT_FIELDS) {
    if (!clone[field] || typeof clone[field] !== 'object' || Array.isArray(clone[field])) {
      clone[field] = {};
    }
  }

  return clone;
};