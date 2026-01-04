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
    // Keep only last 10 entries
    localStorage.setItem('vocalpoint_history', JSON.stringify(history.slice(0, 10)));
    loadHistory();
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
