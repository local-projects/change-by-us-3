define ["underscore", "backbone", "jquery", "template", "moment", "abstract-view", "model/PostReplyModel","model/UserModel"],
	(_, Backbone, $, temp, moment, AbstractView, PostReplyModel, UserModel) ->
		PostReplyView = AbstractView.extend

			tagName: "li"

			initialize: (options) ->
				AbstractView::initialize.call @, options
				@model = new PostReplyModel(options.model)
				@fetch()
			
			onFetch:->
				@viewData = @model.attributes
				@user = new UserModel(id:@model.get("user").id)
				@user.fetch
					success: =>@render()

			render: -> 
				@viewData.image_url_round_small = @user.get("image_url_round_small")
				@viewData.display_name          = @user.get("display_name")
				@viewData.format_date           = moment(@model.get("created_at")).format("MMMM D hh:mm a")

				$reply = $("<div class='post-reply clearfix'/>")
				$reply.template @templateDir+"/templates/partials-universal/post-reply-view.html", 
					{data:@viewData}, => @onTemplateLoad()
				$(@el).append $reply