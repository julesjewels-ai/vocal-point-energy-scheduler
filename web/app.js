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
    medium: { icon: '💧', label: 'Medium Energy' },
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
    for (let i = 0; i < 20; i++) {
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
    const label = recordBtn.querySelector('.label');
    switch (state) {
        case 'recording':
            recordBtn.classList.add('recording');
            recordBtn.setAttribute('aria-pressed', 'true');
            recordBtn.removeAttribute('disabled');
            label.innerHTML = 'Tap to<br>Stop';
            waveform.classList.remove('hidden');
            status.textContent = '🎙️ Listening...';
            break;
        case 'processing':
            recordBtn.classList.remove('recording');
            recordBtn.classList.add('loading');
            recordBtn.setAttribute('aria-pressed', 'false');
            recordBtn.setAttribute('disabled', 'true');
            waveform.classList.add('hidden');
            status.textContent = '⏳ Processing...';
            break;
        case 'ready':
        default:
            recordBtn.classList.remove('recording', 'loading');
            recordBtn.setAttribute('aria-pressed', 'false');
            recordBtn.removeAttribute('disabled');
            label.innerHTML = 'Tap to<br>Record';
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

// Render trend chart using Canvas API with gradient fill
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
    const dpr = window.devicePixelRatio || 1;
    trendChart.width = rect.width * dpr;
    trendChart.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    
    const width = rect.width;
    const height = rect.height;
    const padding = { top: 10, right: 10, bottom: 10, left: 10 };
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get data points (newest first, so reverse for left-to-right chronological)
    const dataPoints = history
        .slice(0, 15)  // Show last 15 entries
        .map(entry => entry.energy_score ?? levelToScore(entry.energy_level))
        .reverse();
    
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;
    const xStep = chartWidth / (dataPoints.length - 1);
    const yScale = chartHeight / 100;
    
    // Build path
    const points = dataPoints.map((score, i) => ({
        x: padding.left + (i * xStep),
        y: padding.top + chartHeight - (score * yScale)
    }));
    
    // Draw filled area with gradient
    const gradient = ctx.createLinearGradient(0, padding.top, 0, height - padding.bottom);
    gradient.addColorStop(0, 'rgba(99, 179, 237, 0.3)');
    gradient.addColorStop(1, 'rgba(99, 179, 237, 0.05)');
    
    ctx.beginPath();
    ctx.moveTo(points[0].x, height - padding.bottom);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, height - padding.bottom);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw line
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        // Smooth curve using quadratic bezier
        const xc = (points[i].x + points[i - 1].x) / 2;
        const yc = (points[i].y + points[i - 1].y) / 2;
        ctx.quadraticCurveTo(points[i - 1].x, points[i - 1].y, xc, yc);
    }
    ctx.lineTo(points[points.length - 1].x, points[points.length - 1].y);
    ctx.strokeStyle = '#63b3ed';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();
    
    // Draw dots
    points.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.strokeStyle = '#63b3ed';
        ctx.lineWidth = 2;
        ctx.stroke();
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
        historyList.innerHTML = '<li class="empty-state">No logs yet. Tap to record!</li>';
        return;
    }

    history.slice(0, 5).forEach(entry => {
        const config = ENERGY_CONFIG[entry.energy_level] || ENERGY_CONFIG.medium;
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="time">${formatTime(entry.timestamp)}</span>
            <span class="separator">-</span>
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
