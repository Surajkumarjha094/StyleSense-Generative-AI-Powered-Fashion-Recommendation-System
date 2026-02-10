document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const photoInput = document.getElementById('photoInput');
    const preview = document.getElementById('preview');
    const previewContainer = document.getElementById('previewContainer');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');
    const btnText = document.getElementById('btnText');
    const alertContainer = document.getElementById('alertContainer');
    const resultsContainer = document.getElementById('resultsContainer');
    const placeholderContainer = document.getElementById('placeholderContainer');
    const loadingContainer = document.getElementById('loadingContainer');
    const loadingPreview = document.getElementById('loadingPreview');

    // Camera Elements
    const uploadTab = document.getElementById('uploadTab');
    const cameraTab = document.getElementById('cameraTab');
    const uploadMode = document.getElementById('uploadMode');
    const cameraMode = document.getElementById('cameraMode');
    const cameraFeed = document.getElementById('cameraFeed');
    const captureCanvas = document.getElementById('captureCanvas');
    const startCameraBtn = document.getElementById('startCameraBtn');
    const captureBtn = document.getElementById('captureBtn');
    const stopCameraBtn = document.getElementById('stopCameraBtn');
    const cameraPreview = document.getElementById('cameraPreview');
    const cameraPreviewContainer = document.getElementById('cameraPreviewContainer');
    const zoomControls = document.getElementById('zoomControls');
    const zoomSlider = document.getElementById('zoomSlider');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomLevel = document.getElementById('zoomLevel');
    const cameraLoading = document.getElementById('cameraLoading');
    
    let currentMode = 'upload';
    let mediaStream = null;
    let capturedImageData = null;
    let currentZoom = 1;
    let lastRecommendationsMarkdown = '';
    let lastProducts = [];
    let lastAnalysisMeta = null;

    // Helper to pick an icon for product cards based on gender
    function getGenderIcon(gender) {
        if (!gender) return '🧑';
        const g = gender.toString().toLowerCase();
        if (g.indexOf('male') !== -1 || g.indexOf('man') !== -1) return '👔';
        if (g.indexOf('female') !== -1 || g.indexOf('woman') !== -1) return '👗';
        return '🧑';
    }

    // Initialize tab styles
    uploadTab.classList.add('active');
    uploadTab.classList.add('btn-secondary');
    uploadTab.classList.remove('btn-outline-secondary');
    cameraTab.classList.add('btn-outline-secondary');

    // Tab Switching
    uploadTab.addEventListener('click', function() {
        currentMode = 'upload';
        uploadTab.classList.add('active');
        uploadTab.classList.remove('btn-outline-secondary');
        uploadTab.classList.add('btn-secondary');
        cameraTab.classList.remove('active');
        cameraTab.classList.add('btn-outline-secondary');
        cameraTab.classList.remove('btn-secondary');
        uploadMode.style.display = 'block';
        cameraMode.style.display = 'none';
        stopCamera();
    });

    cameraTab.addEventListener('click', function() {
        currentMode = 'camera';
        cameraTab.classList.add('active');
        cameraTab.classList.remove('btn-outline-secondary');
        cameraTab.classList.add('btn-secondary');
        uploadTab.classList.remove('active');
        uploadTab.classList.add('btn-outline-secondary');
        uploadTab.classList.remove('btn-secondary');
        uploadMode.style.display = 'none';
        cameraMode.style.display = 'block';
    });

    // Camera Functions
    function startCamera() {
        console.log('🎥 Starting camera...');
        cameraLoading.style.display = 'block';
        cameraFeed.style.display = 'none';
        
        // Request camera with zoom capability
        const constraints = {
            video: {
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 },
                aspectRatio: { ideal: 16 / 9 }
            },
            audio: false
        };
        
        console.log('📹 Requesting camera with constraints:', constraints);
        
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                console.log('✅ Camera stream obtained:', stream);
                mediaStream = stream;
                
                // Assign stream to video element
                cameraFeed.srcObject = stream;
                
                // Wait for video to load
                cameraFeed.onloadedmetadata = function() {
                    console.log('✅ Video metadata loaded');
                    cameraFeed.play().catch(err => {
                        console.error('❌ Play error:', err);
                        showAlert('Could not start camera playback: ' + err.message, 'danger');
                    });
                };
                
                // Show camera after a brief delay
                setTimeout(() => {
                    cameraLoading.style.display = 'none';
                    cameraFeed.style.display = 'block';
                    startCameraBtn.style.display = 'none';
                    captureBtn.style.display = 'block';
                    stopCameraBtn.style.display = 'block';
                    zoomControls.style.display = 'block';
                    currentZoom = 1;
                    zoomSlider.value = 1;
                    updateZoomLevel();
                    console.log('✅ Camera UI updated');
                }, 100);
            })
            .catch(error => {
                console.error('❌ Camera error:', error);
                cameraLoading.style.display = 'none';
                
                let errorMsg = 'Camera access denied. ';
                if (error.name === 'NotAllowedError') {
                    errorMsg += 'Please allow camera permission in browser settings.';
                } else if (error.name === 'NotFoundError') {
                    errorMsg += 'No camera device found.';
                } else if (error.name === 'NotReadableError') {
                    errorMsg += 'Camera is currently unavailable or in use.';
                } else {
                    errorMsg += error.message;
                }
                
                showAlert(errorMsg, 'danger');
            });
    }

    function stopCamera() {
        console.log('🛑 Stopping camera...');
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => {
                console.log('Stopping track:', track.kind);
                track.stop();
            });
            mediaStream = null;
        }
        cameraFeed.style.display = 'none';
        cameraLoading.style.display = 'none';
        captureBtn.style.display = 'none';
        stopCameraBtn.style.display = 'none';
        zoomControls.style.display = 'none';
        startCameraBtn.style.display = 'block';
        currentZoom = 1;
        console.log('✅ Camera stopped');
    }
    
    function updateZoomLevel() {
        currentZoom = parseFloat(zoomSlider.value);
        cameraFeed.style.transform = `scaleX(-1) scale(${currentZoom})`;
        cameraFeed.style.transformOrigin = 'center';
        zoomLevel.textContent = currentZoom.toFixed(1) + 'x';
    }
    
    function capturePhotoWithZoom() {
        const context = captureCanvas.getContext('2d');
        const width = cameraFeed.videoWidth;
        const height = cameraFeed.videoHeight;
        
        captureCanvas.width = width;
        captureCanvas.height = height;
        
        // Draw the video frame
        context.save();
        context.scale(-1, 1);
        context.drawImage(cameraFeed, -width, 0, width, height);
        context.restore();
        
        // Convert to blob with quality compression for face detection
        captureCanvas.toBlob(blob => {
            capturedImageData = blob;
            
            // Create preview
            const reader = new FileReader();
            reader.onload = function(e) {
                cameraPreview.src = e.target.result;
                cameraPreview.style.display = 'block';
                cameraPreviewContainer.classList.add('show');
            };
            reader.readAsDataURL(blob);
            
            stopCamera();
            showAlert('✅ Photo captured! Ready to analyze.', 'success');
        }, 'image/jpeg', 0.95);
    }

    startCameraBtn.addEventListener('click', startCamera);
    stopCameraBtn.addEventListener('click', stopCamera);
    captureBtn.addEventListener('click', capturePhotoWithZoom);
    
    // Zoom Controls
    zoomSlider.addEventListener('input', updateZoomLevel);
    
    zoomOutBtn.addEventListener('click', function() {
        let newZoom = parseFloat(zoomSlider.value) - 0.5;
        if (newZoom < 1) newZoom = 1;
        zoomSlider.value = newZoom;
        updateZoomLevel();
    });
    
    zoomInBtn.addEventListener('click', function() {
        let newZoom = parseFloat(zoomSlider.value) + 0.5;
        if (newZoom > 5) newZoom = 5;
        zoomSlider.value = newZoom;
        updateZoomLevel();
    });

    // Image Preview for File Upload
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
                previewContainer.classList.add('show');
            };
            reader.readAsDataURL(file);
        }
    });

    // Form Submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const gender = document.getElementById('gender').value;
        
        let fileToAnalyze = null;
        let previewSource = null;
        
        if (currentMode === 'upload') {
            fileToAnalyze = photoInput.files[0];
            previewSource = preview.src;
            
            if (!fileToAnalyze) {
                showAlert('Please select a photo', 'danger');
                return;
            }
        } else if (currentMode === 'camera') {
            if (!capturedImageData) {
                showAlert('Please capture a photo from camera', 'danger');
                return;
            }
            fileToAnalyze = capturedImageData;
            previewSource = cameraPreview.src;
        }

        // Disable submit button and show loader
        submitBtn.disabled = true;
        spinner.classList.add('show');
        btnText.textContent = 'Analyzing...';
        alertContainer.innerHTML = '';

        // Show loading animation
        loadingContainer.classList.add('show');
        loadingPreview.src = previewSource;
        resultsContainer.classList.remove('show');
        placeholderContainer.style.display = 'none';

        const formData = new FormData();
        
        // Handle both File objects and Blob objects
        if (fileToAnalyze instanceof Blob) {
            formData.append('file', fileToAnalyze, 'camera_capture.jpg');
        } else {
            formData.append('file', fileToAnalyze);
        }
        
        formData.append('gender', gender);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data);
                showAlert('Analysis complete! Check your personalized style guide below.', 'success');
            } else {
                showAlert(data.message || 'An error occurred', 'danger');
            }
            
            loadingContainer.classList.remove('show');
        } catch (error) {
            const errorMsg = error.message || 'Server error. Please try again.';
            showAlert(errorMsg, 'danger');
            console.error('Error:', error);
            loadingContainer.classList.remove('show');
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            spinner.classList.remove('show');
            btnText.textContent = 'Analyze & Style Me!';
        }
    });

    function showAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        alertContainer.innerHTML = '';
        alertContainer.appendChild(alert);
    }

    function displayResults(data) {
        // Save raw data for download / share
        lastRecommendationsMarkdown = data.recommendations || '';
        lastProducts = data.products || [];
        lastAnalysisMeta = data;

        // Show action buttons
        const resultActions = document.getElementById('resultActions');
        if (resultActions) resultActions.style.display = 'flex';
        // Update skin tone detection
        document.getElementById('skintoneText').textContent = data.skin_tone;
        document.getElementById('colorBox').style.backgroundColor = data.average_color;

        // Update face shape detection
        document.getElementById('faceshapeText').textContent = data.face_shape;

        // Update recommendations
        const recommendationsHtml = markdownToHtml(data.recommendations);
        document.getElementById('recommendationsContent').innerHTML = recommendationsHtml;

        // Update shopping guide
        if (data.products && data.products.length > 0) {
            const shoppingGrid = document.getElementById('shoppingGuide');
            const icon = getGenderIcon(data.gender);
            shoppingGrid.innerHTML = data.products.map(product => `
                <div class="product-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">${icon}</div>
                    <h6>${product.name}</h6>
                    <p class="text-muted" style="font-size: 0.9rem; margin-bottom: 1rem;">${product.description || ''}</p>
                    <a href="${product.shop_link}" target="_blank" class="shop-btn">
                        <span>🛍️</span> Shop Now
                    </a>
                </div>
            `).join('');
        }

        // Show results, hide placeholder
        resultsContainer.classList.add('show');
        placeholderContainer.style.display = 'none';

        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    // Download handler: create a markdown/text file and trigger download
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            if (!lastAnalysisMeta) {
                showAlert('No analysis available to download', 'warning');
                return;
            }

            const lines = [];
            lines.push('# StyleAI — Personalized Style Guide');
            lines.push('');
            lines.push(`Detected Skin Tone: ${lastAnalysisMeta.skin_tone}`);
            lines.push(`Detected Face Shape: ${lastAnalysisMeta.face_shape}`);
            lines.push(`Average Color: ${lastAnalysisMeta.average_color}`);
            lines.push('');
            lines.push('---');
            lines.push('');
            // Append recommendations (markdown returned from server)
            lines.push(lastRecommendationsMarkdown || 'No recommendations available.');
            lines.push('');
            lines.push('---');
            lines.push('');
            if (lastProducts && lastProducts.length > 0) {
                lines.push('Recommended Products:');
                lastProducts.forEach(p => {
                    lines.push(`- ${p.name} — ${p.description || ''}`);
                    if (p.shop_link) lines.push(`  Link: ${p.shop_link}`);
                });
            }

            const blob = new Blob([lines.join('\n')], { type: 'text/markdown;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            a.href = url;
            a.download = `styleai_recommendations_${timestamp}.md`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        });
    }

    // WhatsApp share handler: open wa.me with a concise message (encoded)
    const whatsappBtn = document.getElementById('whatsappBtn');
    if (whatsappBtn) {
        whatsappBtn.addEventListener('click', function() {
            if (!lastAnalysisMeta) {
                showAlert('No analysis available to share', 'warning');
                return;
            }

            // Build a concise share message
            let message = `StyleAI Recommendation:\n`;
            message += `Skin Tone: ${lastAnalysisMeta.skin_tone} -- Face Shape: ${lastAnalysisMeta.face_shape}\\n\\n`;

            // Use the first 600 characters of the recommendations to keep message reasonable
            const rec = (lastRecommendationsMarkdown || '').replace(/\n+/g, '\n').trim();
            const snippet = rec.length > 600 ? rec.slice(0, 600) + '... (truncated)' : rec;
            message += snippet + '\n\n';

            if (lastProducts && lastProducts.length > 0) {
                message += 'Products:\n';
                lastProducts.slice(0,5).forEach(p => {
                    message += `- ${p.name}: ${p.shop_link || ''}\n`;
                });
            }

            const encoded = encodeURIComponent(message);
            const waLink = `https://wa.me/?text=${encoded}`;
            window.open(waLink, '_blank');
        });
    }

    function markdownToHtml(markdown) {
        let html = markdown;

        // Headers
        html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

        // Bold and italic
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
        html = html.replace(/_(.*?)_/g, '<em>$1</em>');

        // Links
        html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Lists
        html = html.replace(/^- (.*?)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*?<\/li>)/s, function(match) {
            return '<ul>' + match + '</ul>';
        });

        // Line breaks
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';

        // Clean up multiple <p> tags
        html = html.replace(/<\/p><p>/g, '</p><p>');

        return html;
    }

    // Smooth scroll to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    /* === Assistant chat widget === */
    const assistantBtn = document.getElementById('assistantBtn');
    const assistantModalEl = document.getElementById('assistantModal');
    const assistantMessages = document.getElementById('assistantMessages');
    const assistantInput = document.getElementById('assistantInput');
    const assistantSendBtn = document.getElementById('assistantSendBtn');
    let assistantModal = null;
    if (assistantModalEl) assistantModal = new bootstrap.Modal(assistantModalEl);

    function appendAssistantMessage(role, text) {
        const wrapper = document.createElement('div');
        wrapper.className = 'mb-2 d-flex';
        if (role === 'user') {
            wrapper.style.justifyContent = 'flex-end';
            wrapper.innerHTML = `<div class="p-2 rounded-3 text-white" style="background:linear-gradient(90deg,#2563eb,#06b6d4);max-width:80%">${escapeHtml(text)}</div>`;
        } else {
            wrapper.style.justifyContent = 'flex-start';
            wrapper.innerHTML = `<div class="p-2 rounded-3 bg-light text-dark" style="max-width:80%">${escapeHtml(text)}</div>`;
        }
        assistantMessages.appendChild(wrapper);
        assistantMessages.scrollTop = assistantMessages.scrollHeight;
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    if (assistantBtn && assistantModal) {
        assistantBtn.addEventListener('click', () => {
            assistantModal.show();
            assistantInput.focus();
        });
    }

    async function sendAssistantQuestion() {
        const q = assistantInput.value.trim();
        if (!q) return;
        appendAssistantMessage('user', q);
        assistantInput.value = '';
        assistantInput.disabled = true;
        assistantSendBtn.disabled = true;

        // typing placeholder
        const typingId = 'typing-' + Date.now();
        const typingEl = document.createElement('div');
        typingEl.className = 'mb-2 d-flex';
        typingEl.style.justifyContent = 'flex-start';
        typingEl.id = typingId;
        typingEl.innerHTML = `<div class="p-2 rounded-3 bg-light text-dark" style="max-width:80%"><em>Thinking...</em></div>`;
        assistantMessages.appendChild(typingEl);
        assistantMessages.scrollTop = assistantMessages.scrollHeight;

        try {
            const resp = await fetch('/api/assistant', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: q })
            });
            const data = await resp.json();
            document.getElementById(typingId)?.remove();
            if (data && data.success) {
                appendAssistantMessage('assistant', data.answer || 'No answer returned.');
            } else {
                appendAssistantMessage('assistant', data.message || 'Sorry, I could not get an answer right now.');
            }
        } catch (err) {
            document.getElementById(typingId)?.remove();
            appendAssistantMessage('assistant', 'Network or server error: ' + (err.message || err));
            console.error('Assistant error', err);
        } finally {
            assistantInput.disabled = false;
            assistantSendBtn.disabled = false;
            assistantInput.focus();
        }
    }

    assistantSendBtn?.addEventListener('click', sendAssistantQuestion);
    assistantInput?.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendAssistantQuestion();
        }
    });
});
