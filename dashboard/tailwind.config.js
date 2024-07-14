/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,js}", "./**/*.{html,js}", "./index.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter var"],
      },
    },
  },
  plugins: [],
};
