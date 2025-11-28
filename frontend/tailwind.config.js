/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1e40af',
          dark: '#1e3a8a',
          light: '#3b82f6',
        },
        secondary: {
          DEFAULT: '#0891b2',
          dark: '#0e7490',
          light: '#06b6d4',
        },
        success: {
          DEFAULT: '#059669',
          light: '#10b981',
          bg: '#d1fae5',
        },
        warning: {
          DEFAULT: '#d97706',
          light: '#f59e0b',
          bg: '#fef3c7',
        },
        danger: {
          DEFAULT: '#dc2626',
          light: '#ef4444',
          bg: '#fee2e2',
        },
        info: {
          DEFAULT: '#0284c7',
          light: '#0ea5e9',
          bg: '#e0f2fe',
        },
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        'sm': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
      },
    },
  },
  plugins: [],
}

