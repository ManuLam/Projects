/**
 * Extends the Annotorious editor with the Semantic Tagging field.
 * @param {Object} annotator the annotator (provided by the Annotorious framework)
 */
var tagstore = [];
annotorious.plugin.SemanticTagging.prototype._extendEditor = function(annotator) {
  var self = this,
  container = document.createElement('div'),
  popupContainer = document.createElement('div');

  container.className = 'semtagging-editor-container';
  popupContainer.className = 'semtagging-popup-container';

        var storetag = [];
        var tagkey = 0;
        var tagbool = false;
        var tagmax = 0;

        function tagFindAnnotations() {
            var tags = anno.getAnnotations();
            if(tagbool == false) {
              for(var i = 0; i < tags.length; i++) {
                storetag[i] = JSON.stringify(tags[i].shapes);
                tagstore[i] = new Array();
                tagmax = i;
              }
            }

            if(tagbool == true) {
              //alert(max +" " + s.length);
              if(tagmax < tags.length) {
                for(var i = tagmax+1; i < tags.length; i++) {
                  storetag[i] = JSON.stringify(tags[i].shapes);
                  tagstore[i] = new Array();
                  tagmax = i;
                }
              }
            }
            tagbool = true;
        }


  // Adds a tag
  var addTag = function(annotation) {
    tagFindAnnotations();

    var link = document.createElement('a');
    link.style.cursor = 'pointer';
    link.className = 'semtagging-tag semtagging-editor-tag';
    link.innerHTML = document.getElementById("fl").value;
    temp = link.innerHTML;

    var jqLink = jQuery(link);
    jqLink.addClass('accepted');

    for(var i = 0; i < storetag.length; i++) {
      try {if(storetag[i] == JSON.stringify(annotation.shapes)) tagkey = i;}
      catch(e){}
    }

    for(var j = 0; j < tagstore[tagkey].length; j++) {
      var clone = tagstore[tagkey][j].cloneNode(true);
      container.appendChild(tagstore[tagkey][j]);
      popupContainer.appendChild(clone);
    }

    if(link.innerHTML != "" && temp != prev1) {
      tagstore[tagkey].push(link);
      container.appendChild(link);
    }


    document.getElementById("fl").value = "";
    prev1 = temp;
  };

    // Add a key listener to Annotorious editor (and binds stuff to it)
  annotator.editor.element.addEventListener('keyup', event => {         
    var annotation = annotator.editor.getAnnotation();
    if(event.key === "Enter")  addTag(annotation);    
  });


  // Final step: adds the field to the editor
  annotator.editor.addField(function(annotation) {
    container.innerHTML = '';

    addTag(annotation);

    return container;
  });

    // Final step: adds the field to the editor
  annotator.popup.addField(function(annotation) {
    popupContainer.innerHTML = '';

    addTag(annotation);

    return popupContainer;
  });

}