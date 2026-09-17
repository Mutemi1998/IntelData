/* ════════════════════════════════════════════════════════
   BILLING & SUBSCRIPTION MANAGEMENT
   ════════════════════════════════════════════════════════ */

/**
 * Store plan prices for toggle functionality
 * This should be populated from the server via data attributes
 */
const planPrices = {};

/**
 * Toggle between monthly and yearly billing
 * @param {boolean} isYearly - True for yearly, false for monthly
 */
function toggleBilling(isYearly) {
  const toggle = document.getElementById('billing-toggle');
  const lblMonthly = document.getElementById('lbl-monthly');
  const lblYearly = document.getElementById('lbl-yearly');

  // Update label colors
  lblMonthly.style.color = isYearly ? 'var(--muted)' : 'var(--text)';
  lblYearly.style.color = isYearly ? 'var(--text)' : 'var(--muted)';

  // Update all plan prices
  document.querySelectorAll('[data-plan-id]').forEach(planEl => {
    const planId = planEl.dataset.planId;
    const priceEl = document.getElementById(`price-${planId}`);
    const savingsEl = document.getElementById(`ysavings-${planId}`);

    if (priceEl && planPrices[planId]) {
      priceEl.innerHTML = isYearly ? planPrices[planId].yearly : planPrices[planId].monthly;
    }

    if (savingsEl) {
      savingsEl.style.display = isYearly ? 'block' : 'none';
    }
  });
}

/**
 * Confirm plan change with modal
 * @param {string} planName - Name of the new plan
 * @param {number} planId - ID of the new plan
 * @param {string} direction - 'upgrade' or 'downgrade'
 */
function confirmPlanChange(planName, planId, direction) {
  const isUpgrade = direction === 'upgrade';

  // Update modal content
  document.getElementById('modal-plan-title').textContent = isUpgrade ? 'Upgrade plan' : 'Downgrade plan';
  document.getElementById('modal-plan-sub').textContent = isUpgrade
    ? 'You are about to upgrade your subscription. New features unlock immediately.'
    : 'You are about to downgrade. Some features may become unavailable.';
  document.getElementById('modal-plan-new').textContent = planName;

  const btn = document.getElementById('modal-plan-btn');
  btn.textContent = isUpgrade ? 'Confirm upgrade' : 'Confirm downgrade';
  btn.className = isUpgrade ? 'btn btn-primary' : 'btn btn-danger';

  // Get URL from data attribute (set by template)
  const urlMap = document.getElementById('plan-urls');
  if (urlMap) {
    const urlSpan = urlMap.querySelector(`[data-plan-id="${planId}"]`);
    if (urlSpan) {
      const form = document.getElementById('plan-change-form');
      form.action = urlSpan.dataset.url;
    }
  }

  openModal('modal-plan-change');
}

/**
 * Scroll to plan section
 */
function scrollToPlan() {
  setTimeout(() => {
    const section = document.getElementById('plans-section');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 50);
}

/**
 * Copy billing plan price to clipboard
 * @param {Element} btn - The button element
 */
function copyText(btn) {
  const box = btn.closest('.key-box');
  if (!box) return;

  const text = box.querySelector('span')?.textContent.trim();
  if (!text) return;

  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard', 'success', 2000);
  }).catch(() => {
    showToast('Failed to copy', 'error');
  });
}

export {
  toggleBilling,
  confirmPlanChange,
  scrollToPlan,
  copyText,
};