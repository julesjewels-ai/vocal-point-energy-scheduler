/**
 * VocalPoint PWA - Audio Recording & Energy Analysis
 */

const API_URL = 'https://vocal-point-energy-scheduler.onrender.com';

// DOM Elements
const recordBtn = document.getElementById('recordBtn');
const waveform = document.getElementById('waveform');
const status = document.getElementById('status');
const resultSection = document.getElementById('result');
const energyIcon = document.getElementById('energyIcon');
const energyLevel = document.getElementById('energyLevel');
const indicators = document.getElementById('indicators');
const historyList = document.getElementById('historyList');
const trendsSection = document.getElementById('trends');
const trendChart = document.getElementById('trendChart');

// State
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

// Energy Level Mapping
const ENERGY_CONFIG = {
    high: { icon: '⚡', label: 'High Energy' },
    medium: { icon: '🌊', label: 'Medium Energy' },
    low: { icon: '☕', label: 'Low Energy' }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    renderTrendChart();
    setupWaveformBars();
});

// Create waveform bars
function setupWaveformBars() {
    for (let i = 0; i < 30; i++) {
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.animationDelay = `${i * 0.05}s`;
        waveform.appendChild(bar);
    }
}

// Record button click handler
recordBtn.addEventListener('click', async () => {
    if (isRecording) {
        stopRecording();
    } else {
        await startRecording();
    }
});

// Start recording
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await analyzeAudio(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        isRecording = true;
        updateUI('recording');
    } catch (error) {
        console.error('Microphone access denied:', error);
        status.textContent = '❌ Microphone access denied';
    }
}

// Stop recording
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        isRecording = false;
        updateUI('processing');
    }
}

// Analyze audio with backend
async function analyzeAudio(audioBlob) {
    status.textContent = '🔍 Analyzing your energy...';

    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        displayResult(result);
        saveToHistory(result);
    } catch (error) {
        console.error('Analysis failed:', error);
        status.textContent = '❌ Analysis failed. Is the server running?';
        updateUI('ready');
    }
}

// Display analysis result
function displayResult(result) {
    const config = ENERGY_CONFIG[result.energy_level] || ENERGY_CONFIG.medium;

    energyIcon.textContent = config.icon;
    energyLevel.textContent = config.label;
    energyLevel.className = `energy-level ${result.energy_level}`;

    // Display indicators
    indicators.innerHTML = '';
    const ind = result.indicators;
    const tags = [
        `Tone: ${ind.tone}`,
        `Pace: ${ind.pace}`,
        `Emotion: ${ind.emotion}`,
        ...ind.non_speech_cues.map(c => `🔊 ${c}`)
    ];
    tags.forEach(tag => {
        const span = document.createElement('span');
        span.className = 'indicator';
        span.textContent = tag;
        indicators.appendChild(span);
    });

    resultSection.classList.remove('hidden');
    updateUI('ready');
}

// Update UI state
function updateUI(state) {
    switch (state) {
        case 'recording':
            recordBtn.classList.add('recording');
            recordBtn.querySelector('.label').textContent = 'Tap to Stop';
            waveform.classList.remove('hidden');
            status.textContent = '🎙️ Listening...';
            break;
        case 'processing':
            recordBtn.classList.remove('recording');
            recordBtn.classList.add('loading');
            waveform.classList.add('hidden');
            status.textContent = '⏳ Processing...';
            break;
        case 'ready':
        default:
            recordBtn.classList.remove('recording', 'loading');
            recordBtn.querySelector('.label').textContent = 'Tap to Record';
            waveform.classList.add('hidden');
            status.textContent = 'Ready to listen';
            break;
    }
}

// Save result to history (localStorage)
function saveToHistory(result) {
    const history = JSON.parse(localStorage.getItem('vocalpoint_history') || '[]');
    history.unshift({
        timestamp: new Date().toISOString(),
        ...result
    });
    // Keep last 100 entries for trend visualization
    localStorage.setItem('vocalpoint_history', JSON.stringify(history.slice(0, 100)));
    loadHistory();
    renderTrendChart();
}

// Render trend chart using Canvas API
function renderTrendChart() {
    const history = JSON.parse(localStorage.getItem('vocalpoint_history') || '[]');
    
    // Need at least 2 points for a trend line
    if (history.length < 2) {
        trendsSection.classList.add('hidden');
        return;
    }
    
    trendsSection.classList.remove('hidden');
    const ctx = trendChart.getContext('2d');
    const rect = trendChart.getBoundingClientRect();
    
    // Set canvas resolution for sharp rendering
    trendChart.width = rect.width * 2;
    trendChart.height = rect.height * 2;
    ctx.scale(2, 2);
    
    const width = rect.width;
    const height = rect.height;
    const padding = 20;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get data points (newest first, so reverse for left-to-right chronological)
    const dataPoints = history
        .slice(0, 20)  // Show last 20 entries
        .map(entry => entry.energy_score ?? levelToScore(entry.energy_level))
        .reverse();
    
    const xStep = (width - padding * 2) / (dataPoints.length - 1);
    const yMin = 0;
    const yMax = 100;
    const yScale = (height - padding * 2) / (yMax - yMin);
    
    // Draw grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    [25, 50, 75].forEach(val => {
        const y = height - padding - (val * yScale);
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    });
    
    // Draw trend line
    ctx.strokeStyle = 'var(--primary)';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, padding, 0, height - padding);
    gradient.addColorStop(0, '#22c55e');  // High energy - green
    gradient.addColorStop(0.5, '#3b82f6');  // Medium - blue
    gradient.addColorStop(1, '#f97316');  // Low - orange
    ctx.strokeStyle = gradient;
    
    ctx.beginPath();
    dataPoints.forEach((score, i) => {
        const x = padding + (i * xStep);
        const y = height - padding - (score * yScale);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Draw data points
    dataPoints.forEach((score, i) => {
        const x = padding + (i * xStep);
        const y = height - padding - (score * yScale);
        
        ctx.fillStyle = score >= 70 ? '#22c55e' : score >= 40 ? '#3b82f6' : '#f97316';
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Convert categorical level to numeric score (fallback for old entries)
function levelToScore(level) {
    switch (level) {
        case 'high': return 80;
        case 'medium': return 50;
        case 'low': return 25;
        default: return 50;
    }
}

// Load history from localStorage
function loadHistory() {
    const history = JSON.parse(localStorage.getItem('vocalpoint_history') || '[]');
    historyList.innerHTML = '';

    if (history.length === 0) {
        historyList.innerHTML = '<li style="text-align:center;color:var(--text-muted);">No logs yet</li>';
        return;
    }

    history.forEach(entry => {
        const config = ENERGY_CONFIG[entry.energy_level] || ENERGY_CONFIG.medium;
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="time">${formatTime(entry.timestamp)}</span>
            <span class="level ${entry.energy_level}">${config.icon} ${config.label}</span>
        `;
        historyList.appendChild(li);
    });
}

// Format timestamp for display
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
