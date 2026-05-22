import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx,mdx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/lib/**/*.{ts,tsx}",
  ],
  darkMode: "media",
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            "max-width": "none",
            a: {
              "text-decoration": "underline",
              "text-underline-offset": "3px",
              "text-decoration-thickness": "1px",
            },
            "code::before": { content: "none" },
            "code::after": { content: "none" },
            code: {
              "font-weight": "500",
              padding: "0.15rem 0.3rem",
              "border-radius": "0.25rem",
              "background-color": "rgba(0,0,0,0.04)",
            },
            "pre code": {
              "background-color": "transparent",
              padding: "0",
            },
          },
        },
      },
    },
  },
  plugins: [typography],
};

export default config;
