// Belief Explorer - Main JavaScript

// Global variables
let conversationHistory = [];
let lastAnalysisData = null;
let radarChart = null;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
  // Initialize elements
  const chatContainer = document.getElementById('chatContainer');
  const userInput = document.getElementById('userInput');
  const sendButton = document.getElementById('sendButton');
  const spinnerContainer = document.getElementById('spinnerContainer');
  const toggleAnalysis = document.getElementById('toggleAnalysis');
  const analysisColumn = document.getElementById('analysisColumn');
  const claimsAnalysis = document.getElementById('claimsAnalysis');
  const perspectivesContent = document.getElementById('perspectivesContent');
  const metricsOverview = document.getElementById('metricsOverview');
  const metricsExplanation = document.getElementById('metricsExplanation');
  const radarChartCanvas = document.getElementById('radarChart');
  const tabs = document.querySelectorAll('.tabs button');
  const tabContents = document.querySelectorAll('.tab-content');

  // Add initial message
  conversationHistory = [
    { role: 'assistant', content: 'What belief or idea would you like to explore together?' }
  ];
  renderConversation();

  // Event Listeners
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tabContents.forEach(content => content.style.display = 'none');

      tab.classList.add('active');
      const tabId = tab.getAttribute('data-tab') + 'Tab';
      document.getElementById(tabId).style.display = 'block';
    });
  });

  toggleAnalysis.addEventListener('click', () => {
    const isHidden = analysisColumn.style.display === 'none' || !analysisColumn.style.display;
    analysisColumn.style.display = isHidden ? 'block' : 'none';
    toggleAnalysis.textContent = isHidden ? 'Hide Analysis' : 'Show Analysis';
  });

  sendButton.addEventListener('click', handleSend);

  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !userInput.disabled) {
      e.preventDefault();
      handleSend();
    }
  });

  // Auto-resize textarea
  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
  });

  // Handle dark mode changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (radarChart) {
      updateRadarChartColors();
    }
  });

  // Initialize theme-based elements
  initializeThemeElements();
});

// Initialize theme-dependent elements
function initializeThemeElements() {
  // This function can be used to set initial theme-dependent elements
  // For example, setting initial radar chart colors if it exists
  if (radarChart) {
    updateRadarChartColors();
  }
}

// Update radar chart colors based on current theme
function updateRadarChartColors() {
  const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)';
  const tickColor = isDarkMode ? '#ccc' : '#666';
  
  if (radarChart) {
    radarChart.options.scales.r.angleLines.color = gridColor;
    radarChart.options.scales.r.grid.color = gridColor;
    radarChart.options.scales.r.pointLabels.color = tickColor;
    radarChart.options.scales.r.ticks.color = tickColor;
    radarChart.update();
  }
}

// Handle send button click
async function handleSend() {
  const text = userInput.value.trim();
  if (!text) return;

  // Add user message to history and render immediately
  conversationHistory.push({ role: 'user', content: text });
  renderConversation();

  // Clear input and disable controls
  userInput.value = '';
  userInput.style.height = 'auto';
  userInput.disabled = true;
  sendButton.disabled = true;
  spinnerContainer.style.display = 'flex';

  try {
    const response = await fetchAnalysis(text);
    
    // Add assistant response to conversation
    conversationHistory.push({ role: 'assistant', content: response.Response });
    renderConversation();
    
    // Process analysis data if available
    if (response.AnalysisJSON) {
      try {
        const analysisData = JSON.parse(response.AnalysisJSON);
        renderAnalysis(analysisData);
      } catch (e) {
        console.error("Error parsing analysis JSON:", e);
      }
    }
  } catch (err) {
    // Handle error
    console.error("API Error:", err);
    conversationHistory.push({ 
      role: 'assistant', 
      content: "I'm sorry, I encountered an error while processing your request. Please try again." 
    });
    renderConversation();
  } finally {
    // Re-enable controls
    userInput.disabled = false;
    sendButton.disabled = false;
    spinnerContainer.style.display = 'none';
    userInput.focus();
  }
}

// Fetch analysis from API
async function fetchAnalysis(statement) {
  // API endpoint will be replaced with actual backend URL
  const API_URL = 'https://api.beliefexplorer.com/api/analyze';
  
  const payload = {
    statement: statement,
    history: conversationHistory.slice(0, -1) // Send history before current message
  };
  
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) {
    let errorText = `Server error: ${response.status} ${response.statusText}`;
    try {
      const errorData = await response.json();
      errorText = errorData.message || JSON.stringify(errorData);
    } catch (e) {
      errorText = await response.text() || errorText;
    }
    throw new Error(errorText);
  }
  
  return await response.json();
}

// Render conversation in chat container
function renderConversation() {
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.innerHTML = '';
  
  conversationHistory.forEach(turn => {
    const div = document.createElement('div');
    div.className = 'message ' + (turn.role === 'assistant' ? 'assistant-message' : 'user-message');
    div.textContent = turn.content;
    chatContainer.appendChild(div);
  });
  
  // Scroll to the bottom
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Render analysis data
function renderAnalysis(analysisData) {
  if (!analysisData || !Array.isArray(analysisData)) {
    console.warn("Invalid analysis data received for rendering:", analysisData);
    renderClaimsAnalysis(null);
    renderPerspectives(null);
    renderAdvancedMetrics(null);
    return;
  }
  
  lastAnalysisData = analysisData;

  // Render all three views
  renderClaimsAnalysis(analysisData);
  renderPerspectives(analysisData);
  renderAdvancedMetrics(analysisData);

  // Show the toggle button and panel
  const toggleAnalysis = document.getElementById('toggleAnalysis');
  const analysisColumn = document.getElementById('analysisColumn');
  
  toggleAnalysis.style.display = 'block';
  analysisColumn.style.display = 'block';
  toggleAnalysis.textContent = 'Hide Analysis';
}

// Render claims analysis
function renderClaimsAnalysis(analysisData) {
  const claimsAnalysis = document.getElementById('claimsAnalysis');
  
  if (!analysisData || !Array.isArray(analysisData) || analysisData.length === 0) {
    claimsAnalysis.innerHTML = '<div class="placeholder">No specific claims were identified for analysis in the last statement.</div>';
    return;
  }

  claimsAnalysis.innerHTML = '';

  analysisData.forEach((item, index) => {
    const claimDiv = document.createElement('div');
    claimDiv.className = 'claim-box';

    // Claim text
    const claimText = document.createElement('div');
    claimText.className = 'claim-text';
    claimText.textContent = `Claim ${index + 1}: ${item.claim || 'N/A'}`;
    claimDiv.appendChild(claimText);

    // Assumption tag
    if (item.assumptions) {
      const assumptionTag = document.createElement('div');
      assumptionTag.className = 'assumption-tag';
      assumptionTag.textContent = item.assumptions;
      claimDiv.appendChild(assumptionTag);
    }

    // Scores (only if verifactScore exists)
    if (item.verifactScore && item.verifactScore.components) {
      const components = item.verifactScore.components;
      const overallScore = item.verifactScore.overallScore;

      // Display Overall Score First (if available)
      if (overallScore != null) {
        appendScoreBar(claimDiv, 'Verifact Score', overallScore);
      }

      // Display Component Scores
      for (const [key, value] of Object.entries(components)) {
        const formattedKey = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
        appendScoreBar(claimDiv, formattedKey, value);
      }
    } else {
      const noScore = document.createElement('div');
      noScore.textContent = 'Detailed scores not available for this claim.';
      noScore.style.fontSize = '12px';
      noScore.style.color = '#888';
      claimDiv.appendChild(noScore);
    }

    claimsAnalysis.appendChild(claimDiv);
  });
}

// Append score bar to parent element
function appendScoreBar(parentDiv, label, value) {
  const numericValue = parseFloat(value);
  if (isNaN(numericValue)) return;

  const scoreName = document.createElement('div');
  scoreName.className = 'score-name';
  scoreName.innerHTML = `<span>${label}</span><span>${(numericValue * 100).toFixed(0)}%</span>`;
  parentDiv.appendChild(scoreName);

  const scoreBar = document.createElement('div');
  scoreBar.className = 'score-bar';
  const scoreFill = document.createElement('div');
  scoreFill.className = 'fill';
  
  // Use setTimeout to trigger animation after element is added to DOM
  setTimeout(() => {
    scoreFill.style.width = (numericValue * 100) + '%';
  }, 50);
  
  scoreBar.appendChild(scoreFill);
  parentDiv.appendChild(scoreBar);
}

// Render perspectives
function renderPerspectives(analysisData) {
  const perspectivesContent = document.getElementById('perspectivesContent');
  
  // Check if the first claim has perspectives
  if (!analysisData || !Array.isArray(analysisData) || analysisData.length === 0 || 
      !analysisData[0].perspectives || analysisData[0].perspectives.length === 0) {
    perspectivesContent.innerHTML = '<div class="placeholder">No alternative perspectives were generated for the primary claim.</div>';
    return;
  }

  perspectivesContent.innerHTML = '';

  // Get the first claim's perspectives
  const item = analysisData[0];

  // Create the perspectives container
  const perspectivesContainer = document.createElement('div');
  perspectivesContainer.className = 'perspectives-container';

  // Add each perspective
  item.perspectives.forEach(perspective => {
    if (!perspective || !perspective.name || !perspective.description || !perspective.assessment) {
      console.warn("Skipping invalid perspective:", perspective);
      return;
    }

    const perspDiv = document.createElement('div');
    perspDiv.className = 'perspective-panel';

    // Perspective title and score
    const titleDiv = document.createElement('div');
    titleDiv.className = 'perspective-title';

    const titleSpan = document.createElement('span');
    titleSpan.textContent = perspective.name;
    titleDiv.appendChild(titleSpan);

    // Add score only if it exists and is a number
    const scoreValue = parseFloat(perspective.score);
    if (!isNaN(scoreValue)) {
      const scoreSpan = document.createElement('span');
      scoreSpan.className = 'perspective-score';
      scoreSpan.textContent = (scoreValue * 100).toFixed(0) + '%';
      titleDiv.appendChild(scoreSpan);
    }

    perspDiv.appendChild(titleDiv);

    // Perspective description
    const descDiv = document.createElement('div');
    descDiv.className = 'perspective-description';
    descDiv.textContent = perspective.description;
    perspDiv.appendChild(descDiv);

    // Perspective assessment
    const assessDiv = document.createElement('div');
    assessDiv.className = 'perspective-assessment';
    assessDiv.textContent = perspective.assessment;
    perspDiv.appendChild(assessDiv);

    perspectivesContainer.appendChild(perspDiv);
  });

  perspectivesContent.appendChild(perspectivesContainer);
}

// Render advanced metrics
function renderAdvancedMetrics(analysisData) {
  const metricsOverview = document.getElementById('metricsOverview');
  const metricsExplanation = document.getElementById('metricsExplanation');
  const radarChartCanvas = document.getElementById('radarChart');
  
  if (!analysisData || !Array.isArray(analysisData) || analysisData.length === 0 || 
      !analysisData[0].verifactScore || !analysisData[0].verifactScore.components) {
    metricsOverview.innerHTML = '<div class="placeholder">No metrics available yet.</div>';
    metricsExplanation.innerHTML = '';
    
    // Clear existing chart if present
    if (radarChart) {
      radarChart.destroy();
      radarChart = null;
    }
    
    radarChartCanvas.style.display = 'none';
    return;
  }

  // Get the first claim's metrics
  const item = analysisData[0];
  const components = item.verifactScore.components;
  const overallScore = parseFloat(item.verifactScore.overallScore || 0);

  // Define the metrics we want to display
  const metricsToShow = {
    'Verifact Score': overallScore,
    'Empirical Verifiability': parseFloat(components.empiricalVerifiability || 0),
    'Logical Consistency': parseFloat(components.logicalConsistency || 0),
    'Falsifiability': parseFloat(components.falsifiability || 0),
    'Model Diversity': parseFloat(components.modelDiversity || 0),
    'Contextual Sensitivity': parseFloat(components.contextualSensitivity || 0),
    'Reflective Index': parseFloat(components.reflectiveIndex || 0)
  };

  // Create metric boxes
  metricsOverview.innerHTML = '';
  Object.entries(metricsToShow).forEach(([title, value]) => {
    // Skip Verifact Score for the boxes, show components
    if (title === 'Verifact Score') return;

    const metricBox = document.createElement('div');
    metricBox.className = 'metric-box';
    metricBox.innerHTML = `
      <div class="metric-title">${title}</div>
      <div class="metric-value">${(value * 100).toFixed(0)}%</div>
    `;
    metricsOverview.appendChild(metricBox);
  });

  // Create Radar Chart
  createRadarChart(metricsToShow);

  // Create metrics explanation
  metricsExplanation.innerHTML = `
    <h4>Metric Descriptions</h4>
    <p><strong>Empirical:</strong> Based on observable evidence.</p>
    <p><strong>Logical:</strong> Internally consistent reasoning.</p>
    <p><strong>Falsifiable:</strong> Can potentially be proven wrong.</p>
    <p><strong>Diversity:</strong> Considers multiple viewpoints.</p>
    <p><strong>Contextual:</strong> Appropriate for the situation.</p>
    <p><strong>Reflective:</strong> Aware of own assumptions/biases.</p>
  `;
}

// Create radar chart
function createRadarChart(metricsToShow) {
  const radarChartCanvas = document.getElementById('radarChart');
  const ctx = radarChartCanvas.getContext('2d');
  
  // Destroy existing chart if it exists
  if (radarChart) {
    radarChart.destroy();
  }
  
  const radarLabels = [
    'Empirical', 'Logical', 'Falsifiable',
    'Diversity', 'Contextual', 'Reflective'
  ];
  
  const radarData = [
    metricsToShow['Empirical Verifiability'] * 100,
    metricsToShow['Logical Consistency'] * 100,
    metricsToShow['Falsifiability'] * 100,
    metricsToShow['Model Diversity'] * 100,
    metricsToShow['Contextual Sensitivity'] * 100,
    metricsToShow['Reflective Index'] * 100
  ];

  // Determine chart colors based on theme
  const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)';
  const tickColor = isDarkMode ? '#ccc' : '#666';
  const pointColor = isDarkMode ? '#4cc9f0' : '#
(Content truncated due to size limit. Use line ranges to read in chunks)