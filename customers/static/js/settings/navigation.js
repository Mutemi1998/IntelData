/* ════════════════════════════════════════════════════════
   NAVIGATION & SECTION MANAGEMENT
   ════════════════════════════════════════════════════════ */

const SECTION_TITLES = {
  profile:               'Organisation profile',
  billing:              'Billing & subscription',
  wazuh:                'Wazuh agents',
  vulnerabilities:      'Vulnerability scans',
  alerts:               'Alert rules',
  'threat-intelligence': 'Threat intelligence',
  users:                'Users & roles',
  integrations:         'Integrations',
  notifications:        'Notifications',
  audit:                'Audit log',
};

/**
 * Show a specific section and hide others
 * @param {string} sectionId - The ID of the section to show
 */
function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll('.section').forEach(section => {
    section.classList.remove('active');
  });

  // Deactivate all nav links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
  });

  // Show the selected section
  const section = document.getElementById(`sec-${sectionId}`);
  if (section) {
    section.classList.add('active');
  }

  // Activate the nav link
  const navLink = document.querySelector(`[data-section="${sectionId}"]`);
  if (navLink) {
    navLink.classList.add('active');
  }

  // Update breadcrumb
  document.getElementById('breadcrumb-text').textContent = SECTION_TITLES[sectionId] || sectionId;

  // Scroll to top
  document.querySelector('.content').scrollTop = 0;
}

/**
 * Initialize navigation on page load
 */
document.addEventListener('DOMContentLoaded', () => {
  // Set active section from data attribute or default to profile
  const activeLink = document.querySelector('.nav-link.active');
  if (activeLink) {
    const sectionId = activeLink.dataset.section;
    showSection(sectionId || 'profile');
  }
});

/**
 * Keyboard shortcut: Esc to close any modals
 */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.open').forEach(backdrop => {
      backdrop.classList.remove('open');
    });
  }
});

export { showSection };