/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Brand: grey + white + orange-fluo
        ink: {
          50: "#F7F7F8",
          100: "#EFEFF1",
          200: "#DDDDE1",
          300: "#BFBFC6",
          400: "#8E8E97",
          500: "#62626A",
          600: "#3F3F45",
          700: "#27272B",
          800: "#1A1A1D",
          900: "#0F0F11",
        },
        fluo: {
          DEFAULT: "#FF6B1A",
          50: "#FFF1E6",
          100: "#FFE0C7",
          200: "#FFC08F",
          300: "#FF9C57",
          400: "#FF7E2E",
          500: "#FF6B1A",
          600: "#E5560A",
          700: "#B84407",
          800: "#7F2F05",
          900: "#4A1B03",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
      boxShadow: {
        glow: "0 0 0 4px rgba(255, 107, 26, 0.15)",
      },
    },
  },
  plugins: [],
};
