/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/templates/**/*.html",
    "./src/static/src/**/*.js",
    "./node_modules/tw-elements/dist/js/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('./node_modules/tw-elements/dist/plugin')
  ],
}
