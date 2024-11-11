$(document).ready(function() {
    // DOM Elements
    const uploadBox = $('#uploadBox');
    const imageInput = $('#imageInput');
    const previewContainer = $('#previewContainer');
    const imagePreview = $('#imagePreview');
    const changeImageBtn = $('#changeImage');
    let currentFile = null;

    // Initialize drag and drop events
    function initializeUpload() {
        uploadBox.on('dragover dragenter', function(e) {
            e.preventDefault();
            e.stopPropagation();
            $(this).addClass('drag-over');
        });

        uploadBox.on('dragleave drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            $(this).removeClass('drag-over');
        });

        uploadBox.on('drop', function(e) {
            e.preventDefault();
            const droppedFile = e.originalEvent.dataTransfer.files[0];
            if (isValidImage(droppedFile)) {
                handleImageUpload(droppedFile);
            }
        });

        // Click to upload
        uploadBox.click(function() {
            imageInput.click();
        });

        // File input change
        imageInput.change(function(e) {
            const file = e.target.files[0];
            if (isValidImage(file)) {
                handleImageUpload(file);
            }
        });

        // Change image button
        changeImageBtn.click(function() {
            resetUpload();
        });
    }

    // Validate image file
    function isValidImage(file) {
        if (!file) {
            alert('Please select a file.');
            return false;
        }
        
        const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!validTypes.includes(file.type)) {
            alert('Please select a valid image file (JPEG, PNG, or GIF).');
            return false;
        }

        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            alert('Please select an image smaller than 5MB.');
            return false;
        }

        return true;
    }

    // Handle image upload
    function handleImageUpload(file) {
        currentFile = file;
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imagePreview.attr('src', e.target.result);
            uploadBox.hide();
            previewContainer.show();
        };

        reader.onerror = function() {
            alert('Error reading file.');
            resetUpload();
        };

        reader.readAsDataURL(file);
    }

    // Reset upload state
    function resetUpload() {
        currentFile = null;
        imageInput.val('');
        imagePreview.attr('src', '');
        previewContainer.hide();
        uploadBox.show();
    }

    // Process Image
    $('#processButton').click(function() {
        processImage('processing');
    });

    // Augment Image
    $('#augmentButton').click(function() {
        processImage('augmentation');
    });

    // Enhance Image
    $('#enhanceButton').click(function() {
        processImage('enhancement');
    });

    // Process image function
    function processImage(type) {
        if (!currentFile) {
            alert('Please select an image first');
            return;
        }

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('type', type);

        // Get selected options
        const checkboxes = getCheckboxesForType(type);
        checkboxes.forEach(option => {
            if ($(`#${option}`).is(':checked')) {
                formData.append(option, 'true');
            }
        });

        // Show progress bar
        const progressBar = $(`#${type}Progress`);
        const progress = progressBar.find('.progress');
        progressBar.show();
        progress.css('width', '0%');

        // Disable button
        const buttonId = `#${type}Button`;
        $(buttonId).prop('disabled', true);

        // Simulate progress
        let progressValue = 0;
        const progressInterval = setInterval(() => {
            progressValue += 5;
            progress.css('width', `${progressValue}%`);
            if (progressValue >= 90) clearInterval(progressInterval);
        }, 100);

        $.ajax({
            url: '/process',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Complete progress bar
                progress.css('width', '100%');
                setTimeout(() => {
                    progressBar.hide();
                    progress.css('width', '0%');
                }, 500);

                displayResults(response, type);
                
                // Switch to appropriate tab
                $(`.tab-button[data-tab="${type}"]`).click();
            },
            error: function(xhr) {
                alert('Error processing image: ' + (xhr.responseJSON?.error || 'Unknown error'));
                progressBar.hide();
            },
            complete: function() {
                clearInterval(progressInterval);
                $(buttonId).prop('disabled', false);
            }
        });
    }

    function getCheckboxesForType(type) {
        const checkboxMap = {
            'processing': ['resize', 'grayscale', 'normalize', 'center_crop'],
            'augmentation': ['random_crop', 'horizontal_flip', 'rotation', 'color_jitter', 
                           'random_erasing', 'elastic_transform', 'noise'],
            'enhancement': ['histogram_equalization', 'adjust_brightness', 'adjust_contrast',
                          'adjust_saturation', 'gaussian_blur', 'solarize', 'posterize', 
                          'adjust_sharpness']
        };
        return checkboxMap[type] || [];
    }

    // Display results function
    function displayResults(results, type) {
        const resultsGrid = $(`#${type}Results .results-grid`);
        resultsGrid.empty();

        // Add original image
        resultsGrid.append(`
            <div class="result-card">
                <h3>Original Image</h3>
                <img src="${$('#imagePreview').attr('src')}" alt="Original">
            </div>
        `);

        // Add processed images
        Object.entries(results).forEach(([key, value]) => {
            const title = key.split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
            
            resultsGrid.append(`
                <div class="result-card">
                    <h3>${title}</h3>
                    <img src="data:image/png;base64,${value}" alt="${title}">
                </div>
            `);
        });

        // Show the results container
        $(`#${type}Results`).addClass('active');
    }

    // Tab switching functionality
    $('.tab-button').click(function() {
        const tabId = $(this).data('tab');
        
        // Update buttons
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
        
        // Update content
        $('.results-container').removeClass('active');
        $(`#${tabId}Results`).addClass('active');
    });

    // Initialize upload functionality
    initializeUpload();
});
