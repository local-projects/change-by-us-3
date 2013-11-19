define(["underscore", "backbone", "jquery", "template", "form", "abstract-view"], function(_, Backbone, $, temp, form, AbstractView) {
  var ProjectEmbedCalendarModalView;
  return ProjectEmbedCalendarModalView = AbstractView.extend({
    initialize: function(options) {
      AbstractView.prototype.initialize.call(this, options);
      this.viewData.id = this.model.id;
      this.viewData.slug = this.model.slug;
      return this.render();
    },
    render: function() {
      var _this = this;
      this.$el = $("<div class='modal-fullscreen'/>");
      this.$el.template(this.templateDir + "/templates/partials-project/project-embed-calendar.html", {
        data: this.viewData
      }, function() {
        return _this.onTemplateLoad();
      });
      return $(this.parent).append(this.$el);
    },
    onTemplateLoad: function() {
      var options,
        _this = this;
      this.$el.find(".close-x").click(function() {
        return _this.$el.remove();
      });
      options = {
        success: function(response) {
          console.log(response);
          if (response.msg.toLowerCase() === "ok") {
            return window.location.reload();
          }
        }
      };
      return this.$el.find('form').ajaxForm(options);
    }
  });
});
