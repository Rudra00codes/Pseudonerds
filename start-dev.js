const { spawn } = require('child_process');
const path = require('path');

// Start the React frontend only
const frontend = spawn('cmd.exe', ['/c', 'cd frontend-react && npm run start'], {
  stdio: 'inherit',
  shell: true,
  cwd: path.resolve(__dirname),
  env: process.env
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('Shutting down...');
  frontend.kill('SIGINT');
  process.exit();
});

console.log('React development server started. Press Ctrl+C to stop.');