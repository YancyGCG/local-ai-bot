export interface RegenerateResponse {
  success: boolean;
  json_template?: Record<string, unknown>;
  error?: string;
}