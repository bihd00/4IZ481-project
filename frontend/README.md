# Frontend

## Stack

- [NodeJS](https://nodejs.org/en/)
- [TypeScript](https://www.typescriptlang.org/)
- [Svelte](https://svelte.dev/)
- [Vite](https://vitejs.dev/)
- [Tailwind](https://tailwindcss.com/)
- [Firebase](https://firebase.google.com/)

## Development

- configure environment variables
  - create `.env` file at the root of the frontend folder
  - add necessary variables
- install NodeJS `18.12.1`
- in your terminal, run:
  - `npm install`
  - `npm run dev`
- source code in `src` folder

## Deployment

- (assumes Google Cloud CLI is installed and configured properly)
- frontend is deployed as a static SPA
- in your terminal, run:
  - `npm run build`
  - `firebase deploy --only hosting`
