define(["underscore", "backbone", "jquery", "template", "moment", "abstract-view", "model/ProjectUpdateModel", "views/partials-project/ProjectPostReplyView"], function(_, Backbone, $, temp, moment, AbstractView, ProjectUpdateModel, ProjectPostReplyView) {
  var ProjectDiscussionThreadItemView;
  return ProjectDiscussionThreadItemView = AbstractView.extend({
    model: ProjectUpdateModel,
    $repliesHolder: null,
    $postRight: null,
    $replyForm: null,
    tagName: "li",
    initialize: function(options_, forceLoad_) {
      AbstractView.prototype.initialize.call(this, options_);
      if (forceLoad_) {
        return this.loadModel();
      } else {
        return this.render();
      }
    },
    loadModel: function() {
      return console.log('loadModel', this.model);
    },
    render: function() {
      var m,
        _this = this;
      m = moment(this.model.attributes.created_at).format("MMMM D hh:mm a");
      this.model.attributes.format_date = m;
      $(this.el).template(this.templateDir + "/templates/partials-project/project-thread-list-item.html", {
        data: this.model.attributes
      }, function() {
        return _this.onTemplateLoad();
      });
      return this;
    },
    onTemplateLoad: function() {
      var $replyToggle, self;
      self = this;
      this.$repliesHolder = $('<ul class="content-wrapper bordered-item np hide"/>');
      this.$postRight = this.$el.find('.update-content');
      $replyToggle = this.$el.find('.reply-toggle').first();
      return $replyToggle.click(function() {});
    }
  });
});