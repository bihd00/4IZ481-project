/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{svelte,js,ts}"], // for unused CSS,
  plugins: [],
  theme: {
    extend: {
      screens: {
        'xs': '440px'
      }
    },
  },
  variants: {
    extend: {},
  },
};
