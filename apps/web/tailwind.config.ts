import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#080b10",
        panel: "#101820",
        line: "#243241",
        mint: "#34d399",
        amber: "#f5c451",
        steel: "#8ca3b7"
      }
    }
  },
  plugins: []
};

export default config;
