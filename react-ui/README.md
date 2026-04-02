# MultiAgent Studio (React)

React frontend connected to the real Python multi-agent backend.

## Run (Real End-to-End)

1. Start backend API in project root:
   - `cd multi-agent-content`
   - `python -m uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload`
2. Start frontend:
   - `cd multi-agent-content/react-ui`
   - `npm install`
   - `npm run dev`

## API Configuration

Create `react-ui/.env` from `.env.example`:

`VITE_API_BASE_URL=http://127.0.0.1:8000`

## Pages

- `/` : Landing page
- `/demo` : Demo workspace running real agents via backend API
- `/architecture` : System architecture and data flow

## Important

- The `/demo` Run Workflow button calls `/api/pipeline-run` and uses live backend execution.
- No hardcoded/mock output is used for final rendering.
