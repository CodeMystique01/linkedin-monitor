// Professional LinkedIn Monitor Data Flow Animation
const steps = [
  {
    id: 'config',
    label: 'Config',
    status: 'Reading config...',
    log: 'Loaded search terms and API keys from .env',
    duration: 1200
  },
  {
    id: 'serpapi',
    label: 'SerpAPI',
    status: 'Searching LinkedIn...',
    log: 'Queried SerpAPI for LinkedIn mentions',
    duration: 1400
  },
  {
    id: 'filter',
    label: 'Filter',
    status: 'Filtering duplicates...',
    log: 'Filtered out previously seen URLs',
    duration: 1200
  },
  {
    id: 'slack',
    label: 'Slack',
    status: 'Sending alert...',
    log: 'Sent alert to Slack channel',
    duration: 1200
  },
  {
    id: 'storage',
    label: 'Storage',
    status: 'Saving URLs...',
    log: 'Saved new URLs to seen_urls.json',
    duration: 1000
  }
];

const nodeIds = steps.map(s => 'node-' + s.id);
const statusIds = steps.map(s => 'status-' + s.id);
const arrowIds = ['arrow-1', 'arrow-2', 'arrow-3', 'arrow-4'];

const dataPacket = document.getElementById('data-packet');
const progressFill = document.getElementById('progress-fill');
const logBox = document.getElementById('log');
const replayBtn = document.getElementById('replay-btn');

let currentStep = 0;
let animating = false;

function resetFlow() {
  // Reset nodes
  nodeIds.forEach(id => {
    const node = document.getElementById(id);
    node.classList.remove('active', 'success', 'error');
  });
  statusIds.forEach(id => {
    const status = document.getElementById(id);
    status.textContent = 'Idle';
    status.className = 'status';
  });
  // Reset arrows
  arrowIds.forEach(id => {
    document.getElementById(id).classList.remove('animated');
  });
  // Reset progress
  progressFill.style.width = '0%';
  // Reset data packet
  dataPacket.style.left = '0px';
  dataPacket.style.opacity = '0';
  // Reset log
  logBox.textContent = '';
  // Enable replay
  replayBtn.disabled = false;
  currentStep = 0;
  animating = false;
}

function log(msg) {
  logBox.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
}

function animateStep(stepIdx) {
  if (stepIdx >= steps.length) {
    // All done
    setTimeout(() => {
      log('✅ Data flow complete!');
      replayBtn.disabled = false;
    }, 600);
    return;
  }
  animating = true;
  replayBtn.disabled = true;
  // Activate node
  const nodeId = nodeIds[stepIdx];
  const statusId = statusIds[stepIdx];
  const node = document.getElementById(nodeId);
  const status = document.getElementById(statusId);
  node.classList.add('active');
  status.textContent = steps[stepIdx].status;
  status.classList.add('active');
  // Move data packet
  moveDataPacketTo(stepIdx, () => {
    // Animate arrow
    if (stepIdx < arrowIds.length) {
      document.getElementById(arrowIds[stepIdx]).classList.add('animated');
    }
    // Log
    log(steps[stepIdx].log);
    // Progress
    progressFill.style.width = ((stepIdx + 1) / steps.length * 100) + '%';
    // Success node
    setTimeout(() => {
      node.classList.remove('active');
      node.classList.add('success');
      status.classList.remove('active');
      status.classList.add('success');
      status.textContent = 'Done';
      // Next step
      setTimeout(() => animateStep(stepIdx + 1), 400);
    }, steps[stepIdx].duration);
  });
}

function moveDataPacketTo(stepIdx, cb) {
  // Show and move the data packet to the node
  const flowRow = document.getElementById('flow-row');
  const nodes = flowRow.querySelectorAll('.node');
  const node = nodes[stepIdx];
  const nodeRect = node.getBoundingClientRect();
  const rowRect = flowRow.getBoundingClientRect();
  // Calculate left offset
  const left = node.offsetLeft + node.offsetWidth / 2 - dataPacket.offsetWidth / 2;
  dataPacket.style.transition = 'left 0.7s cubic-bezier(.4,1.4,.6,1), opacity 0.3s';
  dataPacket.style.opacity = '1';
  dataPacket.style.left = left + 'px';
  // Update label
  dataPacket.textContent = steps[stepIdx].label + ' Data';
  setTimeout(cb, 700);
}

function startFlow() {
  resetFlow();
  setTimeout(() => animateStep(0), 400);
}

replayBtn.addEventListener('click', () => {
  if (!animating) startFlow();
});

// Start on load
window.addEventListener('DOMContentLoaded', () => {
  resetFlow();
  setTimeout(() => animateStep(0), 800);
}); 