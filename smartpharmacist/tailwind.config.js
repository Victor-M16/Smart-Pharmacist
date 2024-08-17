/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/core/**/*.html',
    './core/templates/auth/**/*.html',
    './templates/**/*.hmtl',
    './node_modules/flowbite/**/*.js'
    // Add paths to other apps if necessary
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
};

