/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'custom-gradient': 'linear-gradient(40deg, #556bc0, #c184fa)',
        
      },
      fontFamily: {
        'roboto-condensed': ['"Roboto Condensed"', 'sans-serif'],
      },
      colors:{
        'custom-blue': '#556bc0',
        'custom-purple': '#c184fa',
        'custom-gray': '#f3f4f6',
        'custom-dark': '#1f2937',
        'custom-light': '#f9fafb',
        'custom-red': '#dc2626',
      }
    },
  },
  plugins: [],
}

