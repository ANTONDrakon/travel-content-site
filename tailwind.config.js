/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./site/templates/**/*.html",
    "./docs/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'travel-bg': '#f8f5f0',
        'travel-ink': '#2d2416',
        'travel-charcoal': '#4a4540',
        'travel-teal': '#0d7c66',
        'travel-copper': '#c97d4b',
        'travel-border': '#d9cfc0',
        'travel-meta': '#8a7e72',
        'travel-frame': '#e8e0d6',
      },
      fontFamily: {
        'inter': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
