const { spawn } = require('child_process');
const path = require('path');

// Start the backend
const backend = spawn('cmd.exe', ['/c', 'cd backend && python main.py'], {
  stdio: 'inherit',
  shell: true,
  cwd: path.resolve(__dirname)
});

// Start the frontend
const frontend = spawn('cmd.exe', ['/c', 'npm run dev'], {
  stdio: 'inherit',
  shell: true,
  cwd: path.resolve(__dirname)
});

// Handle process termination
process.on('SIGINT', () => {
  backend.kill('SIGINT');
  frontend.kill('SIGINT');
  process.exit();
});

console.log('Development servers started. Press Ctrl+C to stop.');