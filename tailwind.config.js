module.exports = {
  content: [
    './templates/**/*.html',
    './core/**/*.html',
    './core/**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        'kuripp-theme': {
          'primary': '#3182ce',
          'primary-focus': '#2b6cb0',
          'primary-content': '#ffffff',
          'secondary': '#2d3748',
          'secondary-focus': '#1a202c',
          'secondary-content': '#ffffff',
          'accent': '#4a5568',
          'neutral': '#f7fafc',
          'base-100': '#ffffff',
          'info': '#3182ce',
          'success': '#38a169',
          'warning': '#dd6b20',
          'error': '#e53e3e',
        },
      },
    ],
  },
}
