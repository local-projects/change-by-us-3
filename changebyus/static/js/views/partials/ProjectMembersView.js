define(["underscore", "backbone", "jquery", "template", "views/partials/ProjectSubView"], function(_, Backbone, $, temp, ProjectSubView) {
    
    var ProjectMembersView = ProjectSubView.extend({
        parent:"#project-members",
        render:function(){ 
            this.$el = $("<div class='project-preview'/>");
            this.$el.template(this.templateDir + '/templates/partials-universal/project.html', {data:this.viewData}, function() {});
            $(this.parent).append(this.$el); 
        },
        addOne: function(model) {
            var view = new Partial();//to do 
            this.$el.append(view);
        }
    });

    return ProjectMembersView;
    
});

