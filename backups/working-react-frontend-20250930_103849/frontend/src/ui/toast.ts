// Simple toast implementation
interface ToastOptions {
  duration?: number;
  type?: 'success' | 'error' | 'info';
}

const createToast = (message: string, options: ToastOptions = {}) => {
  const { duration = 3000, type = 'info' } = options;
  
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 10000;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 14px;
    max-width: 300px;
    word-wrap: break-word;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
  }, duration);
};

export const toast = {
  success: (message: string, options?: Omit<ToastOptions, 'type'>) => 
    createToast(message, { ...options, type: 'success' }),
  error: (message: string, options?: Omit<ToastOptions, 'type'>) => 
    createToast(message, { ...options, type: 'error' }),
  info: (message: string, options?: Omit<ToastOptions, 'type'>) => 
    createToast(message, { ...options, type: 'info' }),
};