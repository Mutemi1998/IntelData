/* ════════════════════════════════════════════════════════
   MODAL MANAGEMENT
   ════════════════════════════════════════════════════════ */

/**
 * Open a modal by ID
 * @param {string} modalId - The ID of the modal to open
 */
function openModal(modalId) {
  const backdrop = document.getElementById(modalId);
  if (backdrop) {
    backdrop.classList.add('open');
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }
}

/**
 * Close a modal by ID
 * @param {string} modalId - The ID of the modal to close
 */
function closeModal(modalId) {
  const backdrop = document.getElementById(modalId);
  if (backdrop) {
    backdrop.classList.remove('open');
    // Restore body scroll
    document.body.style.overflow = '';
  }
}

/**
 * Setup modal backdrop click handlers (click outside to close)
 */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        backdrop.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  });
});

export { openModal, closeModal };