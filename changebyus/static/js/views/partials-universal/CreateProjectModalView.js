define(["underscore", "backbone", "jquery", "template", "views/partials-project/ProjectSubView"], 
    function(_, Backbone, $, temp, ProjectSubView) {
    
    var CreateProjectModalView = ProjectSubView.extend({
        render:function(){
            this.$el = $("<div class='project-preview'/>");
            this.$el.template(this.templateDir + '/templates/partials-universal/create-project-modal.html', {data:this.viewData}, function() {});
            $(this.parent).append(this.$el); 
        }
    });

    return CreateProjectModalView;
    
});


