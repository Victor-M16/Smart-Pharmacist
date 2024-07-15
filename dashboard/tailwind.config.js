/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,js}", "./**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter var"],
      },
    },
  },
  plugins: [],
};
