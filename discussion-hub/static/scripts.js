document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for reply buttons
    const replyButtons = document.querySelectorAll('.reply-button');
    
    replyButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const commentId = button.dataset.commentId;
            const replyForm = document.querySelector(`#reply-form-${commentId}`);
            
            if (replyForm) {
                // Toggle the visibility of the reply form
                replyForm.style.display = replyForm.style.display === 'none' || replyForm.style.display === '' ? 'block' : 'none';
            }
        });
    });

    // Add event listener for reply forms
    const replyForms = document.querySelectorAll('.reply-form');
    
    replyForms.forEach(form => {
        form.addEventListener('submit', (event) => {
            // Prevent default form submission
            event.preventDefault();
            
            const formData = new FormData(form);
            const commentId = form.dataset.commentId;
            const content = formData.get('content');
            
            // Submit the reply form via fetch API
            fetch(`/comment/${commentId}/reply`, {
                method: 'POST',
                body: formData,
            }).then(response => response.json())
              .then(data => {
                  // Handle successful response (e.g., append new reply)
                  if (data.success) {
                      // Reload page to display new reply
                      location.reload();
                  } else {
                      // Handle error
                      console.error(data.error);
                  }
              });
        });
    });


    document.addEventListener("DOMContentLoaded", function() {
        const replyButtons = document.querySelectorAll(".reply-button");
        
        replyButtons.forEach(button => {
            button.addEventListener("click", function() {
                const commentId = this.getAttribute("data-comment-id");
                const replyForm = document.getElementById(`reply-form-${commentId}`);
                
                // Toggle the visibility of the reply form
                if (replyForm.style.display === "none" || replyForm.style.display === "") {
                    replyForm.style.display = "block";
                } else {
                    replyForm.style.display = "none";
                }
            });
        });
    });
    

    // Add event listener for comment forms
    const commentForms = document.querySelectorAll('.comment-form');
    
    commentForms.forEach(form => {
        form.addEventListener('submit', (event) => {
            // Prevent default form submission
            event.preventDefault();
            
            const formData = new FormData(form);
            const threadId = form.dataset.threadId;
            const content = formData.get('content');
            
            // Handle form submission (e.g., via fetch API)
            fetch(`/thread/${threadId}/comment`, {
                method: 'POST',
                body: formData,
            }).then(response => response.json())
              .then(data => {
                  // Handle successful response (e.g., append new comment)
                  if (data.success) {
                      // Update the page with new comment
                      location.reload();
                  } else {
                      // Handle error
                      console.error(data.error);
                  }
              });
        });
    });
});
