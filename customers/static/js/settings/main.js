/* ════════════════════════════════════════════════════════
   INTELDATA SETTINGS UI
   Main JavaScript entry point
   ════════════════════════════════════════════════════════ */

// Import all modules
import { showSection } from './navigation.js';
import { openModal, closeModal } from './modals.js';
import {
  showToast,
  showSuccessToast,
  showErrorToast,
  showWarningToast,
  saveAllSettings,
} from './notifications.js';
import {
  toggleBilling,
  confirmPlanChange,
  scrollToPlan,
  copyText,
} from './billing.js';

/**
 * Expose functions to global scope for use in inline handlers
 * (data-* attributes in HTML)
 */
window.showSection = showSection;
window.openModal = openModal;
window.closeModal = closeModal;
window.showToast = showToast;
window.showSuccessToast = showSuccessToast;
window.showErrorToast = showErrorToast;
window.showWarningToast = showWarningToast;
window.saveAllSettings = saveAllSettings;
window.toggleBilling = toggleBilling;
window.confirmPlanChange = confirmPlanChange;
window.scrollToPlan = scrollToPlan;
window.copyText = copyText;

/**
 * Initialize application on DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log('IntelData Settings UI initialized');

  // Populate plan prices from data attributes (if available)
  const priceMap = document.getElementById('plan-price-data');
  if (priceMap) {
    try {
      const prices = JSON.parse(priceMap.textContent);
      Object.assign(window.planPrices || {}, prices);
    } catch (e) {
      console.warn('Could not parse plan prices', e);
    }
  }

  // Initialize animations
  initializeAnimations();

  // Set up form validation
  initializeFormValidation();
});

/**
 * Simple animation initialization
 */
function initializeAnimations() {
  // Fade in sections on load
  document.querySelectorAll('.card').forEach((card, idx) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, idx * 50);
  });
}

/**
 * Form validation
 */
function initializeFormValidation() {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
      // Add your custom validation here
      // e.preventDefault();
    });
  });
}

/**
 * Error handler for unhandled errors
 */
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  showErrorToast('An error occurred. Please try again.');
});

export {
  showSection,
  openModal,
  closeModal,
  showToast,
  saveAllSettings,
  toggleBilling,
  confirmPlanChange,
};

