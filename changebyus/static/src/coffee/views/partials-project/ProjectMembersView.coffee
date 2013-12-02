define ["underscore", "backbone", "jquery", "template", "views/partials-project/ProjectSubView", "views/partials-project/ProjectMemberListItemView"],
	(_, Backbone, $, temp, ProjectSubView, ProjectMemberListItemView) ->
		ProjectMembersView = ProjectSubView.extend
		
			parent: "#project-members"
			team:[]
			members:[]
			$teamList: null
			$memberList: null
			projectID:0
			view:"public"

			initialize: (options) ->
				@isDataLoaded = options.isDataLoaded || @isDataLoaded
				@view         = options.view || @view
				@projectID    = options.projectID || @projectID
				console.log 'options',options
				ProjectSubView::initialize.call(@, options) 

			render: ->
				@$el = $(@parent)
				templateURL = if (@view is "public") then "/templates/partials-project/project-members.html" else "/templates/partials-project/project-members-admin.html"
				@$el.template @templateDir+templateURL, 
					{}, => @onTemplateLoad()

			onTemplateLoad:-> 
				ProjectSubView::onTemplateLoad.call @
				
				@$teamList   = @$el.find("#team-members ul")
				@$memberList = @$el.find("#project-members ul")

				@collection.on('change', =>@addAll())
				@collection.on('remove', =>@addAll())

				if (@view is "public") and (@collection.length > 0) then @onCollectionLoad()

				onPageElementsLoad()

			# override in subview
			addAll: -> 
				@team = []
				@members = []

				console.log '@collection',@collection
				@collection.each (model) => 
					console.log 'model.get("roles',model.get("roles")
					if ("MEMBER" in model.get("roles")) or ("Member" in model.get("roles"))
						@members.push model
					else
						@team.push model

				@$teamList.html('')
				@$memberList.html('')

				if @team.length is 0 
					@$teamList.parent().parent().hide()
				else
					@$teamList.parent().parent().show()
					@$teamList.parent().parent().find('h4').html(@team.length+' Person Team')

				if @members.length is 0
					@$memberList.parent().parent().hide()
				else
					@$memberList.parent().parent().show()
					@$memberList.parent().parent().find('h4').html(@members.length+' Members')

				@addTeam(model) for model in @team
				@addMember(model) for model in @members

				ProjectSubView::addAll.call(@) 
				@isDataLoaded = true

			addTeam: (model_) -> 
				#to do 
				console.log 'addTeam model_',model_
				view = new ProjectMemberListItemView({model:model_, view:@view, projectID:@projectID})
				@$teamList.append view.el

			addMember: (model_) -> 
				#to do 
				console.log 'addMember model_',model_
				view = new ProjectMemberListItemView({model:model_, view:@view, projectID:@projectID})
				@$memberList.append view.el
