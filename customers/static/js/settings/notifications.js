/* ════════════════════════════════════════════════════════
   TOAST NOTIFICATIONS
   ════════════════════════════════════════════════════════ */

let toastTimer = null;

/**
 * Show a toast notification
 * @param {string} message - The message to display
 * @param {string} type - Type: 'success', 'error', 'warning' (default: 'success')
 * @param {number} duration - How long to show in ms (default: 3000)
 */
function showToast(message, type = 'success', duration = 3000) {
  const toastEl = document.getElementById('toast');
  const messageEl = document.getElementById('toast-msg');
  const iconEl = document.querySelector('.toast-icon');

  if (!toastEl || !messageEl) return;

  // Update message
  messageEl.textContent = message;

  // Update icon class
  iconEl.className = `toast-icon ${type}`;

  // Show toast
  toastEl.classList.add('show');

  // Clear existing timer
  clearTimeout(toastTimer);

  // Auto hide
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('show');
  }, duration);
}

/**
 * Convenience methods
 */
function showSuccessToast(msg, duration = 3000) {
  showToast(msg, 'success', duration);
}

function showErrorToast(msg, duration = 3000) {
  showToast(msg, 'error', duration);
}

function showWarningToast(msg, duration = 3000) {
  showToast(msg, 'warning', duration);
}

/**
 * Save all settings (called from topbar button)
 */
function saveAllSettings() {
  const activeSection = document.querySelector('.section.active');
  const title = activeSection ? activeSection.dataset.title : 'Settings';
  showSuccessToast(`${title} saved successfully`);
}

export {
  showToast,
  showSuccessToast,
  showErrorToast,
  showWarningToast,
  saveAllSettings,
};