define ["underscore", "backbone", "jquery", "template", "views/partials-project/ProjectSubView", "views/partials-project/ProjectUpdateFormView", "views/partials-project/ProjectUpdateListItemView"], 
	(_, Backbone, $, temp, ProjectSubView, ProjectUpdateFormView, ProjectUpdateListItemView) ->
		ProjectUpdatesView = ProjectSubView.extend
			parent: "#project-update"

			render: -> 
				@$el = $("<div class='project'/>")
				@$el.template @templateDir + "/templates/partials-project/project-updates.html",
					data: @viewData
				, =>
					@$el.find(".preload").remove()
					@$ul = @$el.find(".updates-container ul")
					
					# temp here for now
					form = new ProjectUpdateFormView({parent: @$el})

				$(@parent).append @$el

			addOne: (model_) ->
				#console.log "ProjectUpdatesView addOne model", model_
				view = new ProjectUpdateListItemView({model: model_})
				@$ul.append(view.render().el) 