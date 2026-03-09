/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#229B83',
        dark: {
          100: '#229B83',
          200: '#42B6A1',
          300: '#69D6C5'
        }
      }
    },
  },
  plugins: [],
}