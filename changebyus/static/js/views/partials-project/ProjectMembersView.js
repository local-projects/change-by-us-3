var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

define(["underscore", "backbone", "jquery", "template", "project-sub-view", "views/partials-project/ProjectMemberListItemView", "views/partials-universal/CreateModalView"], function(_, Backbone, $, temp, ProjectSubView, ProjectMemberListItemView, CreateModalView) {
  var ProjectMembersView;
  return ProjectMembersView = ProjectSubView.extend({
    parent: "#project-members",
    team: [],
    members: [],
    $teamList: null,
    $memberList: null,
    projectID: 0,
    isOwner: false,
    isOwnerOrganizer: false,
    view: "public",
    initialize: function(options_) {
      var options;
      options = options_;
      this.isDataLoaded = options.isDataLoaded || this.isDataLoaded;
      this.view = options.view || this.view;
      this.projectID = options.projectID || this.projectID;
      this.model = options.model || this.model;
      this.isOwner = options.isOwner || this.isOwner;
      this.isOwnerOrganizer = options.isOwnerOrganizer || this.isOwnerOrganizer;
      return ProjectSubView.prototype.initialize.call(this, options);
    },
    events: {
      "click #alpha": "sortClick",
      "click #created": "sortClick",
      "click #how-do-roles": "slideToggle",
      "click #invite-members": "onInviteClick"
    },
    render: function() {
      var templateURL,
        _this = this;
      this.$el = $(this.parent);
      this.viewData = this.model ? this.model.attributes : {};
      this.viewData.isOwnerOrganizer = this.isOwnerOrganizer;
      templateURL = "partials-project/";
      templateURL += this.view === "public" ? "project-members.html" : "project-members-admin.html";
      return this.$el.template(this.templateDir + templateURL, {
        data: this.viewData
      }, function() {
        return _this.onTemplateLoad();
      });
    },
    toggleHeader: function() {
      console.log('toggleHeader @view', this.view);
      if (!(this.view === "public")) {
        if (this.collection.length === 1) {
          return this.$el.find(".no-results ").show();
        } else {
          this.$el.find(".results ").show();
          this.$how = $('.results .content-wrapper');
          return this.$how.hide();
        }
      }
    },
    onTemplateLoad: function() {
      this.$teamList = this.$el.find("#team-members ul");
      this.$memberList = this.$el.find("#project-members ul");
      if ((this.view === "public") && (this.collection.length > 0)) {
        this.onCollectionLoad();
      }
      return ProjectSubView.prototype.onTemplateLoad.call(this);
    },
    sortClick: function(e) {
      this.addAll($(e.currentTarget).attr("id"));
      return false;
    },
    onCollectionLoad: function() {
      var _this = this;
      ProjectSubView.prototype.onCollectionLoad.call(this);
      this.collection.on('change', function() {
        return _this.addAll();
      });
      this.collection.on('remove', function() {
        return _this.addAll();
      });
      return this.toggleHeader();
    },
    slideToggle: function(e) {
      return this.$how.slideToggle();
    },
    onInviteClick: function(e) {
      var config, modal;
      config = {};
      config.viewData = {
        showShare: true,
        success: true,
        data: {
          slug: this.model.get('slug')
        }
      };
      return modal = new CreateModalView(config);
    },
    addAll: function(sort_) {
      var model, sortBy, _i, _j, _len, _len1, _ref, _ref1,
        _this = this;
      if (sort_ == null) {
        sort_ = "alpha";
      }
      this.team = [];
      this.members = [];
      $("#" + sort_).addClass('sort-deactive').removeClass('ul').siblings().removeClass('sort-deactive').addClass('ul');
      if (sort_ === "alpha") {
        sortBy = this.collection.sortBy(function(model) {
          return model.get('last_name');
        });
      } else {
        sortBy = this.collection.sortBy(function(model) {
          return model.get('created_at');
        });
        sortBy.reverse();
      }
      $.each(sortBy, function(k, model) {
        var ownerID, roles;
        if (model.get("active")) {
          roles = model.get("roles");
          ownerID = _this.model ? _this.model.get('owner').id : -1;
          if (roles.length === 0) {
            model.set("roles", ["Owner"]);
          }
          if ((__indexOf.call(roles, "MEMBER") >= 0) || (__indexOf.call(roles, "Member") >= 0)) {
            return _this.members.push(model);
          } else {
            return _this.team.push(model);
          }
        }
      });
      this.$teamList.html('');
      this.$memberList.html('');
      if (this.team.length === 0) {
        this.$teamList.parent().parent().hide();
      } else {
        this.$teamList.parent().parent().show();
        this.$teamList.parent().parent().find('h4').html(this.team.length + ' Person Team');
      }
      if (this.members.length === 0) {
        this.$memberList.parent().parent().hide();
      } else {
        this.$memberList.parent().parent().show();
        this.$memberList.parent().parent().find('h4').html(this.members.length + ' Members');
      }
      _ref = this.team;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        model = _ref[_i];
        this.addTeam(model);
      }
      _ref1 = this.members;
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        model = _ref1[_j];
        this.addMember(model);
      }
      ProjectSubView.prototype.addAll.call(this);
      this.isDataLoaded = true;
      return this.delegateEvents();
    },
    addTeam: function(model_) {
      var view;
      view = new ProjectMemberListItemView({
        model: model_,
        view: this.view,
        projectID: this.projectID
      });
      return this.$teamList.append(view.$el);
    },
    addMember: function(model_) {
      var view;
      view = new ProjectMemberListItemView({
        model: model_,
        view: this.view,
        projectID: this.projectID
      });
      return this.$memberList.append(view.$el);
    }
  });
});
