// LinkedIn Monitor Data Flow Visualization
class LinkedInMonitorVisualization {
    constructor() {
        this.components = {
            config: { name: 'Config', status: 'idle', data: null },
            serpapi: { name: 'SerpAPI', status: 'idle', data: null },
            filter: { name: 'Filter', status: 'idle', data: null },
            slack: { name: 'Slack', status: 'idle', data: null },
            storage: { name: 'Storage', status: 'idle', data: null }
        };
        
        this.dataPackets = [];
        this.isRunning = false;
        this.interval = null;
    }

    // Initialize the visualization
    init() {
        this.createDataFlowContainer();
        this.setupEventListeners();
        this.startSimulation();
    }

    // Create the data flow container
    createDataFlowContainer() {
        const container = document.createElement('div');
        container.id = 'data-flow-simulation';
        container.innerHTML = `
            <div class="simulation-header">
                <h3>🔄 Real-Time Data Flow Simulation</h3>
                <div class="controls">
                    <button id="start-sim" class="sim-btn">▶️ Start</button>
                    <button id="stop-sim" class="sim-btn">⏹️ Stop</button>
                    <button id="reset-sim" class="sim-btn">🔄 Reset</button>
                </div>
            </div>
            <div class="simulation-container">
                <div class="component-track">
                    ${Object.keys(this.components).map(key => `
                        <div class="component-box" id="${key}-box">
                            <div class="component-header">${this.components[key].name}</div>
                            <div class="component-status" id="${key}-status">Idle</div>
                            <div class="component-data" id="${key}-data"></div>
                        </div>
                    `).join('')}
                </div>
                <div class="data-flow-track" id="data-flow-track"></div>
                <div class="log-container" id="log-container">
                    <h4>📋 Activity Log</h4>
                    <div class="log-entries" id="log-entries"></div>
                </div>
            </div>
        `;
        
        // Add styles
        const styles = document.createElement('style');
        styles.textContent = `
            #data-flow-simulation {
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .simulation-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e9ecef;
            }
            
            .controls {
                display: flex;
                gap: 10px;
            }
            
            .sim-btn {
                background: linear-gradient(45deg, #0077B5, #00A0DC);
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }
            
            .sim-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 119, 181, 0.3);
            }
            
            .simulation-container {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 20px;
            }
            
            .component-track {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .component-box {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
                transition: all 0.3s ease;
            }
            
            .component-box.active {
                border-color: #0077B5;
                background: #e3f2fd;
                transform: scale(1.02);
            }
            
            .component-header {
                font-weight: 600;
                color: #0077B5;
                margin-bottom: 5px;
            }
            
            .component-status {
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 5px;
            }
            
            .component-data {
                font-size: 0.8rem;
                color: #888;
                min-height: 20px;
            }
            
            .data-flow-track {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                min-height: 200px;
                position: relative;
                overflow: hidden;
            }
            
            .data-packet {
                position: absolute;
                background: linear-gradient(45deg, #2196f3, #21cbf3);
                color: white;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                white-space: nowrap;
                animation: flowAnimation 3s linear;
            }
            
            @keyframes flowAnimation {
                0% { left: -100px; opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { left: 100%; opacity: 0; }
            }
            
            .log-container {
                grid-column: 1 / -1;
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .log-entries {
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
            }
            
            .log-entry {
                margin-bottom: 5px;
                padding: 3px 0;
                border-bottom: 1px solid #e9ecef;
            }
            
            .log-entry.info { color: #0077B5; }
            .log-entry.success { color: #28a745; }
            .log-entry.warning { color: #ffc107; }
            .log-entry.error { color: #dc3545; }
        `;
        
        document.head.appendChild(styles);
        
        // Insert after the data-flow section
        const dataFlowSection = document.querySelector('.data-flow');
        dataFlowSection.parentNode.insertBefore(container, dataFlowSection.nextSibling);
    }

    // Setup event listeners
    setupEventListeners() {
        document.getElementById('start-sim').addEventListener('click', () => this.startSimulation());
        document.getElementById('stop-sim').addEventListener('click', () => this.stopSimulation());
        document.getElementById('reset-sim').addEventListener('click', () => this.resetSimulation());
    }

    // Start the simulation
    startSimulation() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.log('🚀 Starting LinkedIn Monitor simulation...', 'info');
        
        this.interval = setInterval(() => {
            this.simulateDataFlow();
        }, 3000);
        
        document.getElementById('start-sim').disabled = true;
        document.getElementById('stop-sim').disabled = false;
    }

    // Stop the simulation
    stopSimulation() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        clearInterval(this.interval);
        this.log('⏹️ Simulation stopped', 'warning');
        
        document.getElementById('start-sim').disabled = false;
        document.getElementById('stop-sim').disabled = true;
        
        // Reset component statuses
        Object.keys(this.components).forEach(key => {
            this.updateComponentStatus(key, 'idle', null);
        });
    }

    // Reset the simulation
    resetSimulation() {
        this.stopSimulation();
        this.clearLog();
        this.log('🔄 Simulation reset', 'info');
    }

    // Simulate data flow through the system
    simulateDataFlow() {
        const searchTerms = ['Your Company', 'Your Product', 'Your Name'];
        const randomTerm = searchTerms[Math.floor(Math.random() * searchTerms.length)];
        
        this.log(`🔍 Searching for: "${randomTerm}"`, 'info');
        
        // Step 1: Config
        this.updateComponentStatus('config', 'active', `Search term: "${randomTerm}"`);
        this.createDataPacket(`Search: "${randomTerm}"`);
        
        setTimeout(() => {
            // Step 2: SerpAPI
            this.updateComponentStatus('serpapi', 'active', 'Fetching results...');
            this.createDataPacket('API Call: SerpAPI');
            
            setTimeout(() => {
                const results = Math.floor(Math.random() * 5) + 1;
                this.updateComponentStatus('serpapi', 'success', `Found ${results} results`);
                this.createDataPacket(`Results: ${results} found`);
                
                setTimeout(() => {
                    // Step 3: Filter
                    this.updateComponentStatus('filter', 'active', 'Checking duplicates...');
                    this.createDataPacket('Filter: Checking duplicates');
                    
                    setTimeout(() => {
                        const newResults = Math.floor(Math.random() * results) + 1;
                        this.updateComponentStatus('filter', 'success', `${newResults} new mentions`);
                        this.createDataPacket(`Filtered: ${newResults} new`);
                        
                        if (newResults > 0) {
                            setTimeout(() => {
                                // Step 4: Slack
                                this.updateComponentStatus('slack', 'active', 'Sending alerts...');
                                this.createDataPacket('Slack: Sending alerts');
                                
                                setTimeout(() => {
                                    this.updateComponentStatus('slack', 'success', `${newResults} alerts sent`);
                                    this.createDataPacket('Slack: Alerts sent');
                                    
                                    setTimeout(() => {
                                        // Step 5: Storage
                                        this.updateComponentStatus('storage', 'active', 'Saving URLs...');
                                        this.createDataPacket('Storage: Saving URLs');
                                        
                                        setTimeout(() => {
                                            this.updateComponentStatus('storage', 'success', 'URLs saved');
                                            this.createDataPacket('Storage: Complete');
                                            this.log(`✅ Processed ${newResults} new mentions`, 'success');
                                            
                                            // Reset all components
                                            setTimeout(() => {
                                                Object.keys(this.components).forEach(key => {
                                                    this.updateComponentStatus(key, 'idle', null);
                                                });
                                            }, 1000);
                                        }, 500);
                                    }, 500);
                                }, 500);
                            }, 500);
                        } else {
                            this.log('ℹ️ No new mentions found', 'info');
                            setTimeout(() => {
                                Object.keys(this.components).forEach(key => {
                                    this.updateComponentStatus(key, 'idle', null);
                                });
                            }, 1000);
                        }
                    }, 500);
                }, 500);
            }, 500);
        }, 500);
    }

    // Update component status
    updateComponentStatus(componentKey, status, data) {
        const component = this.components[componentKey];
        component.status = status;
        component.data = data;
        
        const box = document.getElementById(`${componentKey}-box`);
        const statusEl = document.getElementById(`${componentKey}-status`);
        const dataEl = document.getElementById(`${componentKey}-data`);
        
        // Update visual state
        box.className = `component-box ${status}`;
        statusEl.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        dataEl.textContent = data || '';
        
        // Add status-specific styling
        const statusColors = {
            'idle': '#666',
            'active': '#0077B5',
            'success': '#28a745',
            'error': '#dc3545'
        };
        
        statusEl.style.color = statusColors[status] || '#666';
    }

    // Create animated data packet
    createDataPacket(content) {
        const track = document.getElementById('data-flow-track');
        const packet = document.createElement('div');
        packet.className = 'data-packet';
        packet.textContent = content;
        packet.style.top = `${Math.random() * 150 + 25}px`;
        
        track.appendChild(packet);
        
        // Remove packet after animation
        setTimeout(() => {
            if (packet.parentNode) {
                packet.parentNode.removeChild(packet);
            }
        }, 3000);
    }

    // Add log entry
    log(message, type = 'info') {
        const logContainer = document.getElementById('log-entries');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.innerHTML = `[${new Date().toLocaleTimeString()}] ${message}`;
        
        logContainer.appendChild(entry);
        logContainer.scrollTop = logContainer.scrollHeight;
        
        // Limit log entries
        if (logContainer.children.length > 50) {
            logContainer.removeChild(logContainer.firstChild);
        }
    }

    // Clear log
    clearLog() {
        document.getElementById('log-entries').innerHTML = '';
    }
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    const visualization = new LinkedInMonitorVisualization();
    visualization.init();
}); 