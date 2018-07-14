	// Comment stuff
	(function (window, document) {
	  var commentList = document.querySelector('#comment-wrapper .comment-list-container');
	  var commentForm = document.querySelector('#comment-wrapper .comment-list-form');
	  var commentText = commentForm.querySelector('input[type="text"]');

	  function supportsComments(target) {
	    var type = target.getAttribute('data-pdf-annotate-type');
	    return ['point', 'highlight', 'area'].indexOf(type) > -1;
	  }

	  function insertComment(comment) {
	    var child = document.createElement('div');
	    child.className = 'comment-list-item';
	    child.innerHTML = _twitterText2.default.autoLink(_twitterText2.default.htmlEscape(comment.content));

	    commentList.appendChild(child);
	  }

	  function handleAnnotationClick(target) {
	    if (supportsComments(target)) {
	      (function () {
	        var documentId = target.parentNode.getAttribute('data-pdf-annotate-document');
	        var annotationId = target.getAttribute('data-pdf-annotate-id');

	        _2.default.getStoreAdapter().getComments(documentId, annotationId).then(function (comments) {
	          commentList.innerHTML = '';
	          commentForm.style.display = '';
	          commentText.focus();

	          commentForm.onsubmit = function () {
	            _2.default.getStoreAdapter().addComment(documentId, annotationId, commentText.value.trim()).then(insertComment).then(function () {
	              commentText.value = '';
	              commentText.focus();
	            });

	            return false;
	          };

	          comments.forEach(insertComment);
	        });
	      })();
	    }
	  }

	  function handleAnnotationBlur(target) {
	    if (supportsComments(target)) {
	      commentList.innerHTML = '';
	      commentForm.style.display = 'none';
	      commentForm.onsubmit = null;

	      insertComment({ content: 'No comments' });
	    }
	  }