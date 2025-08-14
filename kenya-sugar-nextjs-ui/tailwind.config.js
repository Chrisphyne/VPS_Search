/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'kenya-green': '#006633',
        'kenya-red': '#FF0000',
        'kenya-black': '#000000',
        'sugar-brown': '#8B4513',
        'sugar-light': '#F5F5DC',
      },
      backgroundImage: {
        'kenya-flag': 'linear-gradient(to bottom, #000000 20%, #FF0000 40%, #006633 60%, #FFFFFF 80%)',
        'sugar-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      },
    },
  },
  plugins: [],
};