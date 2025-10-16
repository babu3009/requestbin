function toggleHovercard(id) {
    event.preventDefault();
    var hovercard = document.getElementById('hovercard-' + id);
    hovercard.style.display = ( hovercard.style.display === 'none' || hovercard.style.display == '' ) ? 'block' : 'none';
}

function copyToClipboard(id) {
    // Try to find the curl command in the detail panel first
    var detailContent = document.getElementById('detail-content-' + id);
    var curlCommand = detailContent ? detailContent.querySelector('.curl-command') : null;
    
    // Fall back to hovercard if detail panel not found
    if (!curlCommand) {
        var hovercard = document.getElementById('hovercard-' + id);
        curlCommand = hovercard ? hovercard.querySelector('.code-preview') : null;
    }
    
    if (curlCommand) {
        var text = curlCommand.innerText;
        navigator.clipboard.writeText(text).then(function() {
            // Visual feedback
            var btn = event.target.closest('button');
            if (btn) {
                var originalText = btn.innerHTML;
                btn.innerHTML = '<i class="icon-ok"></i> Copied!';
                btn.classList.add('btn-success');
                setTimeout(function() {
                    btn.innerHTML = originalText;
                    btn.classList.remove('btn-success');
                }, 2000);
            }
        });
    }
}

function showRequestDetail(requestId) {
    // Remove active class from all list items
    var listItems = document.querySelectorAll('.request-list-item');
    listItems.forEach(function(item) {
        item.classList.remove('active');
    });
    
    // Add active class to clicked item
    var activeItem = document.getElementById('list-item-' + requestId);
    if (activeItem) {
        activeItem.classList.add('active');
    }
    
    // Hide all detail content
    var detailContents = document.querySelectorAll('.request-detail-content');
    detailContents.forEach(function(content) {
        content.classList.remove('active');
    });
    
    // Show selected detail content
    var activeDetail = document.getElementById('detail-content-' + requestId);
    if (activeDetail) {
        activeDetail.classList.add('active');
    }
}

function refreshRequests() {
    // Get the current URL
    var currentUrl = window.location.href;
    
    // Visual feedback - show loading state
    var refreshBtn = event.target.closest('button');
    if (refreshBtn) {
        var originalHTML = refreshBtn.innerHTML;
        refreshBtn.innerHTML = '<i class="icon-refresh icon-spin"></i> Refreshing...';
        refreshBtn.disabled = true;
        
        // Reload the page
        window.location.reload();
    } else {
        // Fallback if button not found
        window.location.reload();
    }
}

// Dropdown menu functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle dropdown toggles
    var dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(function(dropdown) {
        var toggle = dropdown.querySelector('.dropdown-toggle');
        var menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            // Toggle dropdown on click
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other dropdowns
                document.querySelectorAll('.dropdown').forEach(function(otherDropdown) {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('open');
                    }
                });
                
                // Toggle current dropdown
                dropdown.classList.toggle('open');
            });
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(function(dropdown) {
                dropdown.classList.remove('open');
            });
        }
    });
    
    // Close dropdown when pressing Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.dropdown').forEach(function(dropdown) {
                dropdown.classList.remove('open');
            });
        }
    });
});

