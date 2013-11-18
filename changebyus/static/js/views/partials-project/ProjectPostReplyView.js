define(["underscore", "backbone", "jquery", "template", "moment", "abstract-view", "model/ProjectPostReplyModel"], function(_, Backbone, $, temp, moment, AbstractView, ProjectPostReplyModel) {
  var ProjectPostReplyView;
  return ProjectPostReplyView = AbstractView.extend({
    tagName: "li",
    initialize: function(options) {
      AbstractView.prototype.initialize.call(this, options);
      this.model = new ProjectPostReplyModel({
        id: options.id
      });
      return this.render();
    },
    render: function() {
      var $reply,
        _this = this;
      $reply = $("<div class='post-reply clearfix'/>");
      $reply.template(this.templateDir + "/templates/partials-project/project-post-reply-view.html", {
        data: {}
      }, function() {
        return _this.onTemplateLoad();
      });
      return $(this.el).append($reply);
    }
  });
});
