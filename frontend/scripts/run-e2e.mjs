import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'


const scriptDir = dirname(fileURLToPath(import.meta.url))
const frontendDir = dirname(scriptDir)
const viteCli = join(frontendDir, 'node_modules', 'vite', 'bin', 'vite.js')
const playwrightCli = join(
  frontendDir,
  'node_modules',
  '@playwright',
  'test',
  'cli.js',
)
const baseUrl = 'http://127.0.0.1:5180'

const sleep = (milliseconds) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds))

async function waitForServer() {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try {
      const response = await fetch(baseUrl)
      if (response.ok) return
    } catch {
      // Retry while Vite starts.
    }
    await sleep(250)
  }
  throw new Error('Vite test server did not start')
}

function waitForExit(child) {
  return new Promise((resolve, reject) => {
    child.once('error', reject)
    child.once('exit', (code, signal) => resolve({ code, signal }))
  })
}

const server = spawn(
  process.execPath,
  [
    viteCli,
    '--host',
    '127.0.0.1',
    '--port',
    '5180',
    '--strictPort',
  ],
  {
    cwd: frontendDir,
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
  },
)

let serverOutput = ''
server.stdout.on('data', (chunk) => {
  serverOutput += chunk.toString()
})
server.stderr.on('data', (chunk) => {
  serverOutput += chunk.toString()
})

let exitCode = 1
try {
  await waitForServer()
  const testProcess = spawn(
    process.execPath,
    [playwrightCli, 'test'],
    {
      cwd: frontendDir,
      stdio: 'inherit',
      windowsHide: true,
    },
  )
  const result = await waitForExit(testProcess)
  exitCode = result.code ?? 1
} catch (error) {
  console.error(error.message)
  console.error(serverOutput)
} finally {
  server.kill()
  await Promise.race([waitForExit(server), sleep(2000)])
  if (server.exitCode === null && server.signalCode === null) {
    server.kill('SIGKILL')
  }
}

process.exit(exitCode)

