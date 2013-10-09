define(["underscore", "backbone", "jquery", "template", "abstract-view"], function(_, Backbone, $, temp, AbstractView) {
  var ProjectPartialsView;
  return ProjectPartialsView = AbstractView.extend({
    initialize: function(options) {
      AbstractView.prototype.initialize.call(this, options);
      return this.render();
    },
    render: function() {
      var _this = this;
      this.$el = $("<li class='project-preview'/>");
      return this.$el.template(this.templateDir + "/templates/partials-universal/project.html", {
        data: this.model.attributes
      }, function() {
        return console.log('done');
      });
    }
  });
});
